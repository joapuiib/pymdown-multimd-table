'''Shared test utilities for pymdownx_multimd_table tests.'''

from __future__ import annotations

from html.parser import HTMLParser

import markdown


def convert(src: str, extensions: list[str] | None = None, **ext_config) -> str:
    exts = extensions or ['pymdown_multimd_table']
    md = markdown.Markdown(
        extensions=exts,
        extension_configs={'pymdown_multimd_table': ext_config} if ext_config else {},
    )
    return md.convert(src)


def assert_html(
    src: str,
    expected: str,
    extensions: list[str] | None = None,
    **ext_config,
) -> None:
    assert normalize_html(convert(src, extensions=extensions, **ext_config)) == normalize_html(expected)


class _HTMLNormaliser(HTMLParser):
    """Converts HTML into a canonical, whitespace-insensitive form."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        sorted_attrs = sorted(attrs, key=lambda a: a[0])
        attr_str = "".join(
            f' {n}="{v}"' if v is not None else f" {n}"
            for n, v in sorted_attrs
        )
        self._parts.append(f"<{tag}{attr_str}>")

    def handle_endtag(self, tag: str) -> None:
        self._parts.append(f"</{tag}>")

    def handle_data(self, data: str) -> None:
        text = " ".join(data.split())  # collapse all whitespace
        if text:
            self._parts.append(text)

    def result(self) -> str:
        return "".join(self._parts)


def normalize_html(html: str) -> str:
    """Return a normalised, whitespace-collapsed HTML string for comparison."""
    parser = _HTMLNormaliser()
    parser.feed(html.strip())
    return parser.result()
