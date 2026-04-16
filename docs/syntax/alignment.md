# Text Alignment

Column alignment is controlled by placing colons (`:`) in the separator row.

| Separator | Alignment |
| :-------: | :-------- |
| `---`     | Default (no alignment style) |
| `:---`    | Left      |
| `:---:`   | Centre    |
| `---:`    | Right     |

## No alignment

[[% set example_1 %]]
| A | B |
| - | - |
| 1 | 2 |
[[% endset %]]
[[ table_example(example_1) ]]

## Left alignment

[[% set example_2 %]]
| Item     |
| :------- |
| Apple    |
| Banana   |
[[% endset %]]
[[ table_example(example_2) ]]

## Centre alignment

[[% set example_3 %]]
| Score  |
| :----: |
| 42     |
| 100    |
[[% endset %]]
[[ table_example(example_3) ]]

## Right alignment

[[% set example_4 %]]
| Price  |
| -----: |
| $9.99  |
| $14.99 |
[[% endset %]]
[[ table_example(example_4) ]]

## Mixed alignment

[[% set example_5 %]]
| Item      | Value  | Qty  |
| :-------- | -----: | :--: |
| Computer  | $1600  |  1   |
| Phone     |   $12  |  5   |
| Pipe      |    $1  | 200  |
[[% endset %]]
[[ table_example(example_5) ]]

!!! note
    Alignment from the separator row applies to **every** body row in the column,
    including the header cell.
