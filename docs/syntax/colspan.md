# Column Spanning

A cell is merged with the previous cell in the same row by leaving the cell **completely empty**
(no spaces — just consecutive pipe characters `||`).

Each additional `|` adds one more column to the span:

| Syntax | Result |
| :----- | :----- |
| `cell ||` | `colspan="2"` |
| `cell |||` | `colspan="3"` |

## Colspan in the header

```
|            | Grouping  ||
| Header     | A         | B         |
| ---------- | :-------: | --------: |
| Data       | 1         | 2         |
```

/// html | div.result
|            | Grouping  ||
| Header     | A         | B         |
| ---------- | :-------: | --------: |
| Data       | 1         | 2         |
///

## Colspan in the body

```
| A | B | C |
| - | - | - |
| spans   |||
| 1 | 2 | 3 |
```

/// html | div.result
| A | B | C |
| - | - | - |
| spans   |||
| 1 | 2 | 3 |
///

## Colspan combined with alignment

The alignment of the **leftmost** spanned column is applied to the merged cell.

```
|              | Grouping      ||
| Header       | A             | B             |
| :----------- | :-----------: | ------------: |
| Row 1        | spans (centre)||
| Row 2        | centre        | right         |
```

/// html | div.result
|              | Grouping      ||
| Header       | A             | B             |
| :----------- | :-----------: | ------------: |
| Row 1        | spans (centre)||
| Row 2        | centre        | right         |
///

!!! warning "Empty vs. whitespace"
    Only a **strictly empty** cell slice (no characters at all) triggers colspan.
    A cell containing only spaces is a regular empty-content cell.

    ```
    | A  | B  |
    | -  | -  |
    | 1  |    |
    ```

    /// html | div.result
    | A  | B  |
    | -  | -  |
    | 1  |    |
    ///
