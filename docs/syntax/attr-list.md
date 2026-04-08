# Attribute Lists

!!! info "Optional feature"
    Attribute lists require `attr_list: true` in your configuration.

    ```yaml
    markdown_extensions:
      - pymdown_multimd_table:
          attr_list: true
    ```

You can apply HTML attributes to individual **cells** or entire **rows** using
`{…}` blocks that follow the same syntax as the standard
[`attr_list`](https://python-markdown.github.io/extensions/attr_list/) extension:

| Token | Effect |
| :---- | :----- |
| `.class` | Adds a CSS class |
| `#id` | Sets the `id` attribute |
| `key="value"` | Sets an arbitrary HTML attribute |

## Cell attributes

Place `{…}` **inside the cell**, before the closing `|`:

```
| Header                           |
| :------------------------------- |
| plain cell                       |
| styled cell {.highlight}         |
| id cell {#cell-1}                |
| full {#c2 .bold data-x="1"}      |
```

/// html | div.result
| Header                           |
| :------------------------------- |
| plain cell                       |
| styled cell {.highlight}         |
| id cell {#cell-1}                |
| full {#c2 .bold data-x="1"}      |
///

Multiple classes accumulate:

```
| H |
| - |
| multi-class {.c1 .c2} |
```

/// html | div.result
| H |
| - |
| multi-class {.c1 .c2} |
///

## Header cell attributes

Attributes can also be applied to `<th>` cells:

```
| Name {.col-name} | Value {.col-value} |
| :--------------- | :----------------- |
| foo              | 42                 |
```

/// html | div.result
| Name {.col-name} | Value {.col-value} |
| :--------------- | :----------------- |
| foo              | 42                 |
///

## Row attributes

Place `{…}` **after the last `|`** of a row (no space between `|` and `{`):

```
| A | B |
| - | - |
| x | y |{.even}
| p | q |{.odd #row-2}
```

/// html | div.result
| A | B |
| - | - |
| x | y |{.even}
| p | q |{.odd #row-2}
///

## Cell and row attributes combined

Both can be used on the same row simultaneously:

```
| H                       |
| :---------------------- |
| cell {.myclass} |{.myrow}
```

/// html | div.result
| H                       |
| :---------------------- |
| cell {.myclass} |{.myrow}
///

## Header row attributes

Row attributes can be applied to header rows too:

```
| A {.hdr-a} | B {.hdr-b} |{.hdr-row}
| ---------- | ---------- |
| 1          | 2          |
```

/// html | div.result
| A {.hdr-a} | B {.hdr-b} |{.hdr-row}
| ---------- | ---------- |
| 1          | 2          |
///

## Combined with multibody

Row and cell attributes work across all `<tbody>` sections:

```
| H |
| - |
| a |{.even}
| b |{.odd}

| c |{.even}
| d |{.odd}
```

<div class="result" markdown="1">
| H |
| - |
| a |{.even}
| b |{.odd}

| c |{.even}
| d |{.odd}
</div>

Cell attributes equally work per-tbody:

```
| A      | B      |
| :----- | :----- |
| x {.cls1} | y  |

| z      | w {.cls2} |
```

<div class="result" markdown="1">
| A      | B      |
| :----- | :----- |
| x {.cls1} | y  |

| z      | w {.cls2} |
</div>

## Combined with colspan

Cell attributes on a spanning cell are preserved:

```
| A | B | C |
| - | - | - |
| wide {.wide} || x |{.myrow}
```

/// html | div.result
| A | B | C |
| - | - | - |
| wide {.wide} || x |{.myrow}
///

## Combined with rowspan

Cell attributes on a rowspan cell are preserved:

```
| A     | B |
| ----- | - |
| tall {.cls} | 1 |{.row1}
| ^^    | 2 |{.row2}
```

/// html | div.result
| A     | B |
| ----- | - |
| tall {.cls} | 1 |{.row1}
| ^^    | 2 |{.row2}
///

## Combined with wrappable columns

A custom class is **appended** to the `extend` class added by `+` in the separator:

```
| H          |
| :----------+ |
| cell {.myclass} |
```

/// html | div.result
| H          |
| :----------+ |
| cell {.myclass} |
///

## Tbody attributes

Place a standalone `{…}` line **after the last row of a tbody section** (before the blank line separator) to apply attributes to that `<tbody>` element:

```
| Category | Item   | Price |
| :------- | :----- | ----: |
| Fruit    | Apple  | $0.50 |
| Fruit    | Banana | $0.30 |
{.fruit}

| Veggie   | Carrot | $0.80 |
| Veggie   | Onion  | $0.60 |
{.vegetable}
```

<div class="result" markdown="1">
| Category | Item   | Price |
| :------- | :----- | ----: |
| Fruit    | Apple  | $0.50 |
| Fruit    | Banana | $0.30 |
{.fruit}

| Veggie   | Carrot | $0.80 |
| Veggie   | Onion  | $0.60 |
{.vegetable}
</div>

!!! tip "Requires multibody"
    Tbody attributes are only meaningful when `multibody: true` is also set.

## Table attributes

Place a standalone `{…}` line **at the very end of the table block** (as the last line, with no blank line after it) to apply attributes to the `<table>` element:

```
| H |
| - |
| cell |
{#my-table .styled data-x="y"}
```

/// html | div.result
| H |
| - |
| cell |
{#my-table .styled data-x="y"}
///

!!! note "Last `{…}` is always table-level"
    The final `{…}` line of the table block is always treated as a **table-level**
    attribute. All earlier `{…}` lines (before a blank-line separator) are
    **tbody-level** attributes.

    To apply attrs to **both** the last tbody **and** the table, use two
    consecutive `{…}` lines at the end — the first targets the last `<tbody>`,
    the second targets `<table>`:

    ```
    | H |
    | - |
    | row |
    {.last-tbody}
    {.whole-table}
    ```



## Disabled (default)

With `attr_list: false` (the default), `{…}` is rendered as **literal text**:

- `{…}` inside a cell → appears as cell content.
- `{…}` after the last `|` → becomes an extra cell.
- `{…}` on a standalone line → not consumed by the table parser.

!!! tip
    The `attr_list` option is fully compatible with the standard `attr_list`
    Markdown extension. You can enable both simultaneously:

    ```yaml
    markdown_extensions:
      - pymdown_multimd_table:
          attr_list: true
      - attr_list
    ```
