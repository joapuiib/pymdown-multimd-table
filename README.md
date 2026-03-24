# pymdown-multimd-table

A Python-Markdown extension implementing **MultiMarkdown 6** extended table syntax,
mirroring the feature set of the [`markdown-it-multimd-table`](https://github.com/RedBug312/markdown-it-multimd-table) JavaScript plugin.

## Features

### Standard (always enabled)

| Feature | Syntax |
| ------- | ------ |
| Column spanning (colspan) | Empty cells `\|\|` extend the previous cell |
| Text alignment | `:---`, `:---:`, `---:` in the separator |
| Wrappable columns | `---+` in the separator adds `class="extend"` |
| Multiple header rows | Multiple rows before the separator |
| Table captions | `[caption text]` or `[caption text][label]` |
| Multiple tbody sections | Blank line between data rows (see `multibody`) |
| Inline Markdown | Bold, italic, code, etc. inside cells |

### Optional (controlled by config)

| Option | Default | Description |
| ------ | ------- | ----------- |
| `rowspan` | `False` | `^^` in a cell merges it with the cell above |
| `multiline` | `False` | Backslash `\` at end of row continues cell content on the next row |
| `headerless` | `False` | Tables without a header/separator row |
| `multibody` | `True` | Blank lines between data rows create separate `<tbody>` elements |
| `autolabel` | `True` | Auto-generate `id` from caption text |
| `attr_list` | `False` | Parse `{.class #id key=val}` attribute blocks on cells and rows |

## Installation

```bash
pip install pymdown-multimd-table
```

## Usage

```python
import markdown

md = markdown.Markdown(extensions=["pymdown_multimd_table"])
html = md.convert(source)
```

With options:

```python
md = markdown.Markdown(
    extensions=["pymdown_multimd_table"],
    extension_configs={
        "pymdown_multimd_table": {
            "rowspan": True,
            "multiline": True,
            "headerless": True,
            "multibody": True,   # default
            "autolabel": True,   # default
        }
    },
)
```

In **MkDocs** (`mkdocs.yml`):

```yaml
markdown_extensions:
  - pymdown_multimd_table:
      rowspan: true
      multiline: true
```

## Syntax Examples

### Basic table

```
First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
```

<table>
  <thead>
    <tr>
      <th>First Header</th>
      <th>Second Header</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Content Cell</td>
      <td>Content Cell</td>
    </tr>
  </tbody>
</table>


### Alignment

```
| Item      | Value  |
| :-------: | -----: |
| Centered  | Right  |
```

<table>
  <thead>
    <tr>
      <th style="text-align: center;">Item</th>
      <th style="text-align: right;">Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="text-align: center;">Centered</td>
      <td style="text-align: right;">Right</td>
    </tr>
  </tbody>
</table>

### Column spanning

```
|            | Grouping ||
| Header     | A        | B        |
| ---------- | :------: | -------: |
| Data       | spans    ||
```

<table>
  <thead>
    <tr>
      <th></th>
      <th colspan="2">Grouping</th>
    </tr>
    <tr>
      <th>Header</th>
      <th style="text-align: center;">A</th>
      <th style="text-align: right;">B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Data</td>
      <td colspan="2">spans</td>
    </tr>
  </tbody>
</table>


### Caption with label

```
[Sales Data][sales]
| Q1   | Q2   |
| ---- | ---- |
| 100  | 120  |
```

<table>
  <caption id="sales">Sales Data</caption>
  <thead>
    <tr>
      <th>Q1</th>
      <th>Q2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>100</td>
      <td>120</td>
    </tr>
  </tbody>
</table>


### Row spanning (`rowspan: true`)

```
| A      | B  | C  |
| ------ | -- | -- |
| tall   | 1  | x  |
| ^^     | 2  | y  |
```

<table>
  <thead>
    <tr>
      <th>A</th>
      <th>B</th>
      <th>C</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="2">tall</td>
      <td>1</td>
      <td>x</td>
    </tr>
    <tr>
      <td>2</td>
      <td>y</td>
    </tr>
  </tbody>
</table>


### Multiline cells (`multiline: true`)

```
| Code            | Output  |
| --------------- | ------- |
| ```python      |         |\
| print("hello") | hello   |\
| ```            |         |
```

<table>
  <thead>
    <tr>
      <th>Code</th>
      <th>Output</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><pre><code>```python
print("hello")
```</code></pre></td>
      <td>hello</td>
    </tr>
  </tbody>
</table>


### Headerless table (`headerless: true`)

```
| -------- | ----- |
| No header| here  |
```

<table>
  <tbody>
    <tr>
      <td>No header</td>
      <td>here</td>
    </tr>
  </tbody>
</table>


### Attribute lists on cells and rows (`attr_list: true`)

Place a `{…}` block at the end of a cell to add HTML attributes to that cell.
The block supports `.class`, `#id`, and `key="value"` tokens — the same syntax
as the standard [attr_list](https://python-markdown.github.io/extensions/attr_list/)
Markdown extension.

**Cell attributes** — append `{…}` inside the cell, before the closing `|`:

```
| Header                        |
| ----------------------------- |
| plain cell                    |
| styled cell {.highlight}      |
| id cell {#cell-1}             |
| full {#c2 .bold data-x="1"}   |
```

```html
<table>
  <thead>
    <tr><th>Header</th></tr>
  </thead>
  <tbody>
    <tr><td>plain cell</td></tr>
    <tr><td class="highlight">styled cell</td></tr>
    <tr><td id="cell-1">id cell</td></tr>
    <tr><td id="c2" class="bold" data-x="1">full</td></tr>
  </tbody>
</table>
```

**Row attributes** — append `{…}` after the last `|` of a row:

```
| A | B |
| - | - |
| x | y |{.even}
| p | q |{.odd #row-2}
```

```html
<table>
  <thead>
    <tr><th>A</th><th>B</th></tr>
  </thead>
  <tbody>
    <tr class="even"><td>x</td><td>y</td></tr>
    <tr class="odd" id="row-2"><td>p</td><td>q</td></tr>
  </tbody>
</table>
```

**Combined** — cell and row attributes can be used together:

```
| H                  |
| ------------------ |
| cell {.myclass} |{.myrow}
```

```html
<table>
  <thead>
    <tr><th>H</th></tr>
  </thead>
  <tbody>
    <tr class="myrow"><td class="myclass">cell</td></tr>
  </tbody>
</table>
```



## Development

```bash
pip install -e ".[dev]"
pytest tests/
```

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
