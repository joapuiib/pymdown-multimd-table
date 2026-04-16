# Column Spanning

A cell is merged with the previous cell in the same row by leaving the cell **completely empty**
(no spaces — just consecutive pipe characters `||`).

Each additional `|` adds one more column to the span:

| Syntax | Result |
| :----- | :----- |
| `cell ||` | `colspan="2"` |
| `cell |||` | `colspan="3"` |

## Colspan in the header

[[% set example_1 %]]
|            | Grouping  ||
| Header     | A         | B         |
| ---------- | :-------: | --------: |
| Data       | 1         | 2         |
[[% endset %]]
[[ table_example(example_1) ]]

## Colspan in the body

[[% set example_2 %]]
| A | B | C |
| - | - | - |
| spans   |||
| 1 | 2 | 3 |
[[% endset %]]
[[ table_example(example_2) ]]

## Colspan combined with alignment

The alignment of the **leftmost** spanned column is applied to the merged cell.

[[% set example_3 %]]
|              | Grouping      ||
| Header       | A             | B             |
| :----------- | :-----------: | ------------: |
| Row 1        | spans (centre)||
| Row 2        | centre        | right         |
[[% endset %]]
[[ table_example(example_3) ]]

!!! warning "Empty vs. whitespace"
    Only a **strictly empty** cell slice (no characters at all) triggers colspan.
    A cell containing only spaces is a regular empty-content cell.

    [[% set example_4 %]]
    | A  | B  |
    | -  | -  |
    | 1  |    |
    [[% endset %]]
    [[ table_example(example_4) | indent(width=4, first=True, blank=True) ]]
