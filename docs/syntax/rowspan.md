# Row Spanning

!!! info "Optional feature"
    Row spanning requires `rowspan: true` in your configuration.

    ```yaml
    markdown_extensions:
      - pymdown_multimd_table:
          rowspan: true
    ```

Place `^^` in a body cell to merge it **upward** with the cell directly above.
Consecutive `^^` markers keep extending the rowspan.

## Simple rowspan

[[% set example_1 %]]
| A      | B  | C  |
| :----- | :- | :- |
| tall   | 1  | x  |
| ^^     | 2  | y  |
[[% endset %]]
[[ table_example(example_1) ]]

## Three-row span

[[% set example_2 %]]
| A      | B  |
| :----- | :- |
| big    | 1  |
| ^^     | 2  |
| ^^     | 3  |
[[% endset %]]
[[ table_example(example_2) ]]

## Rowspan and colspan combined

[[% set example_3 %]]
| A ||  |
| --- | --- | --- |
| B  | C  | D  |
| ^^ | E  | F  |
| G  || H  |
| ^^ || I  |
| ^^ || J  |
[[% endset %]]
[[ table_example(example_3) ]]

## Notes

- `^^` is only recognised in **body** rows. In a header row it is treated as
  literal text.
- With `rowspan: false` (the default), `^^` is rendered as literal cell content.
