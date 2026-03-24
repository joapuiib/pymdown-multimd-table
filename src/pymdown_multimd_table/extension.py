"""Core implementation of the MultiMarkdown table extension for Python-Markdown.

Architecture mirrors the markdown-it-multimd-table plugin:
  1. A DFA validates the line sequence and collects structural metadata.
  2. The metadata is used to build an ElementTree representing the table.

DFA alphabet constants (encoded as powers-of-16 for precedence ordering):
  CAP = 0x10000  caption
  SEP = 0x01000  separator row
  HDR = 0x00100  header row
  DAT = 0x00010  data row
  EMP = 0x00001  empty line

States are bitmasks of the alphabets that are still *accepted* from that state.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as etree

from markdown import Extension
from markdown.blockprocessors import BlockProcessor

try:
    from markdown.extensions.attr_list import get_attrs as _md_get_attrs
except ImportError:  # pragma: no cover
    _md_get_attrs = None

# ---------------------------------------------------------------------------
# DFA alphabet constants
# ---------------------------------------------------------------------------
CAP = 0x10000
SEP = 0x01000
HDR = 0x00100
DAT = 0x00010
EMP = 0x00001

_SEP_RE = re.compile(r"^:?(-+|=+):?\+?$")
_CAP_RE = re.compile(r"^\[(.+?)\](\[([^\[\]]+)\])?\s*$")
_ATTR_RE = re.compile(r"\s*\{([^}\n]*)\}\s*$")


# ---------------------------------------------------------------------------
# Attribute helpers
# ---------------------------------------------------------------------------


def _apply_attrs(attr_str: str, el: etree.Element) -> None:
    """Apply the inner content of a ``{…}`` attribute block to *el*.

    Uses ``markdown.extensions.attr_list.get_attrs`` when available so that
    the parsing behaviour is identical to the rest of the document.
    """
    if _md_get_attrs is not None:
        for k, v in _md_get_attrs(attr_str):
            if k == ".":
                cls = el.get("class")
                el.set("class", f"{cls} {v}" if cls else v)
            else:
                el.set(k, v)
        return
    # Minimal fallback when attr_list module is unavailable.  # pragma: no cover
    for token in attr_str.split():
        if token.startswith("."):
            cls = el.get("class", "")
            el.set("class", (cls + " " + token[1:]).strip())
        elif token.startswith("#"):
            el.set("id", token[1:])
        elif "=" in token:
            k, _, v = token.partition("=")
            el.set(k, v.strip('"').strip("'"))


def _split_cell_attrs(text: str) -> tuple[str, str | None]:
    """Strip a trailing ``{…}`` block from *text*.

    Returns ``(clean_text, attr_inner)`` on success, ``(text, None)`` otherwise.
    """
    m = _ATTR_RE.search(text)
    if m:
        return text[: m.start()], m.group(1)
    return text, None


def _split_row_attrs(line: str) -> tuple[str, str | None]:
    """Strip a trailing ``{…}`` block that follows the last real pipe in *line*.

    Returns ``(clean_line, attr_inner)`` on success, ``(line, None)`` otherwise.
    Only a ``{…}`` block that is the *sole* content after the last pipe is
    recognised as row-level attributes; anything else is treated as a cell.
    """
    stripped = line.rstrip()
    n = len(stripped)
    bounds = _scan_bound_indices(stripped)
    if not bounds:
        return line, None
    last_pipe = max(
        (b for b in bounds if 0 <= b < n and stripped[b] == "|"),
        default=-1,
    )
    if last_pipe < 0:
        return line, None
    tail = stripped[last_pipe + 1 :]
    m = _ATTR_RE.fullmatch(tail)
    if m:
        return line[: last_pipe + 1], m.group(1)
    return line, None


# ---------------------------------------------------------------------------
# Line-level parsing helpers
# ---------------------------------------------------------------------------


def _scan_bound_indices(line: str) -> list[int]:
    """Return pipe character positions in *line*, skipping escaped pipes and
    pipes inside backtick code spans.

    The list is padded with virtual boundary positions so that every cell
    between consecutive bounds ``(bounds[i], bounds[i+1])`` can be extracted
    as ``stripped[bounds[i]+1 : bounds[i+1]]``.

    Returns an empty list when no valid pipe is found.
    """
    stripped = line.rstrip()
    head = len(line) - len(line.lstrip())
    end = len(stripped)

    bounds: list[int] = []
    escaped = False
    code = False
    serial = 0  # expected backtick-run length when inside a code span

    pos = 0
    while pos < end:
        ch = stripped[pos]

        if ch == "\\":
            escaped = True
            pos += 1
            continue

        if ch == "`":
            # Determine the length of this consecutive backtick run.
            run_end = pos
            while run_end + 1 < end and stripped[run_end + 1] == "`":
                run_end += 1
            run_len = run_end - pos + 1
            if run_len > 1:
                if not code:
                    if serial == 0:
                        serial = run_len
                    elif serial == run_len:
                        serial = 0
                pos = run_end
            else:
                # Single backtick toggles a code span.
                if code or (not escaped and serial == 0):
                    code = not code
            escaped = False
            pos += 1
            continue

        if ch == "|":
            if not code and not escaped:
                bounds.append(pos)
            escaped = False
            pos += 1
            continue

        escaped = False
        pos += 1

    if not bounds:
        return bounds

    # Pad with virtual boundaries to capture leading/trailing cell content.
    if bounds[0] > head:
        bounds.insert(0, head - 1)
    if bounds[-1] < end - 1:
        bounds.append(end)

    return bounds


def _parse_separator(line: str) -> dict | None:
    """Validate and parse a table separator row.

    Returns ``{'aligns': [...], 'wraps': [...]}`` on success, ``None`` on
    failure.  Lines indented by 4+ spaces are treated as code blocks and
    rejected.
    """
    indent = len(line) - len(line.lstrip())
    if indent >= 4:
        return None

    bounds = _scan_bound_indices(line)
    if len(bounds) < 2:
        return None

    stripped = line.rstrip()
    aligns: list[str] = []
    wraps: list[bool] = []

    for c in range(len(bounds) - 1):
        cell = stripped[bounds[c] + 1 : bounds[c + 1]].strip()
        if not _SEP_RE.match(cell):
            return None

        wrap = cell[-1] == "+"
        wraps.append(wrap)

        has_left = cell[0] == ":"
        # When the wrappable marker (+) is present, check the char before it.
        right_idx = -2 if wrap else -1
        has_right = len(cell) > (1 if not wrap else 2) and cell[right_idx] == ":"

        if has_left and has_right:
            aligns.append("center")
        elif has_left:
            aligns.append("left")
        elif has_right:
            aligns.append("right")
        else:
            aligns.append("")

    return {"aligns": aligns, "wraps": wraps}


def _parse_caption(line: str, autolabel: bool) -> dict | None:
    """Parse a caption line of the form ``[text]`` or ``[text][label]``.

    Returns ``{'text': str, 'label': str | None}`` on success, ``None``
    otherwise.
    """
    m = _CAP_RE.match(line.strip())
    if not m:
        return None

    text = m.group(1)
    label: str | None = None

    if autolabel or m.group(2):
        raw = m.group(3) if m.group(2) else m.group(1)
        label = re.sub(r"\W+", "", raw.lower())

    return {"text": text, "label": label}


def _parse_row(line: str, multiline: bool) -> dict | None:
    """Parse a header or data row.

    Returns ``{'bounds': [...], 'multiline': bool}`` when the line contains at
    least two valid pipe boundaries, ``None`` otherwise.

    When *multiline* is enabled a trailing backslash marks the row as a
    continuation line; the bounds are then calculated on the content before
    the backslash.
    """
    stripped = line.rstrip()

    if multiline and stripped.endswith("\\"):
        is_multiline = True
        trimmed = stripped[:-1].rstrip()
        bounds = _scan_bound_indices(trimmed)
    else:
        is_multiline = False
        bounds = _scan_bound_indices(line)

    if len(bounds) < 2:
        return None

    return {"bounds": bounds, "multiline": is_multiline}


# ---------------------------------------------------------------------------
# Block processor
# ---------------------------------------------------------------------------


class MultimdTableProcessor(BlockProcessor):
    """Block processor that parses MultiMarkdown extended table syntax."""

    def __init__(self, parser, config: dict) -> None:
        super().__init__(parser)
        self.config = config

    # ------------------------------------------------------------------
    # BlockProcessor interface
    # ------------------------------------------------------------------

    def test(self, parent: etree.Element, block: str) -> bool:
        lines = block.split("\n")
        if len(lines) < 2:
            return False

        has_pipe_row = False
        has_sep = False
        for line in lines:
            if len(_scan_bound_indices(line)) >= 2:
                has_pipe_row = True
                if _parse_separator(line) is not None:
                    has_sep = True

        if self.config["headerless"]:
            return has_pipe_row
        return has_pipe_row and has_sep

    def run(self, parent: etree.Element, blocks: list[str]) -> bool | None:
        block = blocks.pop(0)
        lines = block.split("\n")

        meta = self._execute_dfa(lines)
        if meta is None:
            blocks.insert(0, block)
            return False

        # With multibody enabled, greedily consume continuation data blocks.
        if self.config["multibody"]:
            while blocks:
                next_lines = blocks[0].split("\n")
                if not self._is_continuation(next_lines):
                    break
                extended = lines + [""] + next_lines
                ext_meta = self._execute_dfa(extended)
                if ext_meta is None:
                    break
                blocks.pop(0)
                lines = extended
                meta = ext_meta

        self._build_table(parent, meta)
        return None

    # ------------------------------------------------------------------
    # DFA execution
    # ------------------------------------------------------------------

    def _match_alphabet(self, state: int, line: str) -> int:
        """Return the highest-precedence alphabet that matches *line* in
        *state*, or ``0`` when no alphabet matches.
        """
        opts = self.config
        for alph in (CAP, SEP, HDR, DAT, EMP):
            if not (state & alph):
                continue
            if alph == CAP:
                if _parse_caption(line, opts["autolabel"]) is not None:
                    return CAP
            elif alph == SEP:
                if _parse_separator(line) is not None:
                    return SEP
            elif alph in (HDR, DAT):
                if _parse_row(line, opts["multiline"]) is not None:
                    return alph
            elif alph == EMP:
                if not line.strip():
                    return EMP
        return 0

    def _execute_dfa(self, lines: list[str]) -> dict | None:
        """Validate *lines* against the MultiMarkdown table DFA and collect
        structural metadata.

        Returns a metadata dict on success or ``None`` when the line sequence
        is not a valid MultiMarkdown table.
        """
        opts = self.config

        transitions: dict[int, dict[int, int]] = {
            0x10100: {CAP: 0x00100, HDR: 0x01100},
            0x00100: {HDR: 0x01100},
            0x01100: {SEP: 0x10010, HDR: 0x01100},
            0x10010: {CAP: 0x00000, DAT: 0x10011},
            0x10011: {CAP: 0x00000, DAT: 0x10011, EMP: 0x10010},
        }
        initial = 0x10100

        if opts["headerless"]:
            initial = 0x11100
            transitions[0x11100] = {CAP: 0x01100, SEP: 0x10010, HDR: 0x01100}

        if not opts["multibody"]:
            transitions[0x10010] = {CAP: 0x00000, DAT: 0x10010}

        accept = {0x10010, 0x10011, 0x00000}

        meta: dict = {"sep": None, "cap": None, "tr": []}
        grp = 0x10
        mtr = -1
        tr_token: dict | None = None
        state = initial

        for i, line in enumerate(lines):
            alph = self._match_alphabet(state, line)
            if alph == 0:
                break

            # --- Actions ---------------------------------------------------
            if alph == CAP:
                if meta["cap"] is None:
                    cap = _parse_caption(line, opts["autolabel"])
                    if cap is not None:
                        cap["first"] = i == 0
                        meta["cap"] = cap

            elif alph == SEP:
                meta["sep"] = _parse_separator(line)
                if tr_token is not None:
                    tr_token["grp"] |= 0x01
                grp = 0x10
                mtr = -1  # separator terminates any open multiline sequence

            elif alph in (HDR, DAT):
                raw_line = line
                row_attrs = None
                if opts["attr_list"]:
                    raw_line, row_attrs = _split_row_attrs(line)
                row = _parse_row(raw_line, opts["multiline"])
                tr_token = {
                    "raw_line": raw_line,
                    "type": alph,
                    "grp": grp,
                    "bounds": row["bounds"],
                    "multiline": row["multiline"],
                    "mbounds": None,
                    "mlines": None,
                    "row_attrs": row_attrs,
                }
                grp = 0x00
                meta["tr"].append(tr_token)

                # Multiline row merging.
                if opts["multiline"]:
                    if tr_token["multiline"] and mtr < 0:
                        mtr = len(meta["tr"]) - 1
                    elif not tr_token["multiline"] and mtr >= 0:
                        first = meta["tr"][mtr]
                        first["mbounds"] = [t["bounds"] for t in meta["tr"][mtr:]]
                        first["mlines"] = [t["raw_line"] for t in meta["tr"][mtr:]]
                        # Row attrs belong to the last (non-continuation) line.
                        first["row_attrs"] = first["row_attrs"] or tr_token["row_attrs"]
                        meta["tr"] = meta["tr"][: mtr + 1]
                        mtr = -1

            elif alph == EMP:
                if tr_token is not None:
                    tr_token["grp"] |= 0x01
                grp = 0x10

            # --- Transition ------------------------------------------------
            state = transitions.get(state, {}).get(alph, 0)

        if state not in accept:
            return None
        if not meta["tr"]:
            return None

        # The last row always closes its group.
        meta["tr"][-1]["grp"] |= 0x01
        return meta

    # ------------------------------------------------------------------
    # Element-tree construction
    # ------------------------------------------------------------------

    def _build_table(
        self, parent: etree.Element, meta: dict
    ) -> etree.Element:
        """Build and append the ``<table>`` element to *parent*."""
        table = etree.SubElement(parent, "table")
        sep = meta["sep"]
        cap = meta["cap"]

        if cap:
            caption_el = etree.SubElement(table, "caption")
            if cap.get("label") is not None:
                caption_el.set("id", cap["label"])
            if not cap["first"]:
                caption_el.set("style", "caption-side: bottom")
            caption_el.text = cap["text"]

        up_tokens: list[etree.Element | None] = []
        tgroup: etree.Element | None = None

        for tr_data in meta["tr"]:
            if tr_data["grp"] & 0x10:
                tag = "thead" if tr_data["type"] == HDR else "tbody"
                tgroup = etree.SubElement(table, tag)
                up_tokens = []  # reset per thead/tbody group

            tr_el = etree.SubElement(tgroup, "tr")  # type: ignore[arg-type]
            if tr_data.get("row_attrs"):
                _apply_attrs(tr_data["row_attrs"], tr_el)
            self._fill_row(tr_el, tr_data, sep, up_tokens)

        return table

    def _fill_row(
        self,
        tr_el: etree.Element,
        tr_data: dict,
        sep: dict | None,
        up_tokens: list[etree.Element | None],
    ) -> None:
        """Populate *tr_el* with th/td child elements for *tr_data*."""
        bounds = tr_data["bounds"]
        stripped = tr_data["raw_line"].rstrip()
        left_cell: etree.Element | None = None

        for c in range(len(bounds) - 1):
            cell_text = stripped[bounds[c] + 1 : bounds[c + 1]]

            # Empty slice between two pipes → colspan: extend the previous cell.
            if cell_text == "":
                if left_cell is not None:
                    colspan = int(left_cell.get("colspan", "1"))
                    left_cell.set("colspan", str(colspan + 1))
                continue

            # ^^ → rowspan: merge with the cell directly above.
            if (
                self.config["rowspan"]
                and c < len(up_tokens)
                and up_tokens[c] is not None
                and cell_text.strip() == "^^"
            ):
                above = up_tokens[c]
                rowspan = int(above.get("rowspan", "1"))  # type: ignore[union-attr]
                above.set("rowspan", str(rowspan + 1))  # type: ignore[union-attr]
                left_cell = None
                continue

            cell_tag = "th" if tr_data["type"] == HDR else "td"
            cell_el = etree.SubElement(tr_el, cell_tag)

            if sep and c < len(sep["aligns"]) and sep["aligns"][c]:
                cell_el.set("style", f"text-align:{sep['aligns'][c]}")
            if sep and c < len(sep["wraps"]) and sep["wraps"][c]:
                existing = cell_el.get("class", "")
                cell_el.set("class", (existing + " extend").strip())

            cell_attrs = None
            if self.config["attr_list"]:
                cell_text, cell_attrs = _split_cell_attrs(cell_text)
            if cell_attrs:
                _apply_attrs(cell_attrs, cell_el)

            if tr_data.get("mbounds") and tr_data.get("mlines"):
                self._fill_multiline_cell(cell_el, c, tr_data)
            else:
                cell_el.text = cell_text.strip()

            left_cell = cell_el
            while len(up_tokens) <= c:
                up_tokens.append(None)
            up_tokens[c] = cell_el

    def _fill_multiline_cell(
        self, cell_el: etree.Element, c: int, tr_data: dict
    ) -> None:
        """Parse multi-line cell content as block Markdown into *cell_el*."""
        cell_lines: list[str] = []

        for mline, mbounds_b in zip(tr_data["mlines"], tr_data["mbounds"]):
            if c >= len(mbounds_b) - 1:
                continue
            raw = mline.rstrip()
            if raw.endswith("\\"):
                raw = raw[:-1].rstrip()
            segment = raw[mbounds_b[c] + 1 : mbounds_b[c + 1]].rstrip()
            cell_lines.append(segment)

        if self.config["attr_list"] and cell_lines:
            cell_lines[-1], cell_attrs = _split_cell_attrs(cell_lines[-1])
            if cell_attrs:
                _apply_attrs(cell_attrs, cell_el)

        self.parser.parseChunk(cell_el, "\n".join(cell_lines))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _is_continuation(self, lines: list[str]) -> bool:
        """Return ``True`` when *lines* look like a table-body continuation:
        they contain pipe rows but no separator and no caption.
        """
        if not lines:
            return False
        if _parse_caption(lines[0], self.config["autolabel"]) is not None:
            return False
        has_pipe = False
        for line in lines:
            if len(_scan_bound_indices(line)) >= 2:
                has_pipe = True
                if _parse_separator(line) is not None:
                    return False
        return has_pipe


# ---------------------------------------------------------------------------
# Extension entry point
# ---------------------------------------------------------------------------


class MultimdTableExtension(Extension):
    """Python-Markdown extension for MultiMarkdown 6 table syntax."""

    def __init__(self, **kwargs: object) -> None:
        self.config = {
            "multiline": [
                False,
                "Allow multiline cells with backslash line continuation (default: False)",
            ],
            "rowspan": [
                False,
                "Enable ^^ syntax for row spanning (default: False)",
            ],
            "headerless": [
                False,
                "Allow tables without a header/separator row (default: False)",
            ],
            "multibody": [
                True,
                "Allow multiple <tbody> sections divided by blank lines (default: True)",
            ],
            "autolabel": [
                True,
                "Auto-generate IDs from caption text (default: True)",
            ],
            "attr_list": [
                False,
                "Parse {.class #id key=val} attributes on cells and rows (default: False)",
            ],
        }
        super().__init__(**kwargs)

    def extendMarkdown(self, md) -> None:
        md.registerExtension(self)
        if "|" not in md.ESCAPED_CHARS:
            md.ESCAPED_CHARS.append("|")
        md.parser.blockprocessors.register(
            MultimdTableProcessor(md.parser, self.getConfigs()),
            "multimd-table",
            80,  # Higher priority than built-in table (75).
        )


def makeExtension(**kwargs: object) -> MultimdTableExtension:
    return MultimdTableExtension(**kwargs)
