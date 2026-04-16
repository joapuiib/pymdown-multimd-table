# Headerless Tables

!!! info "Optional feature"
    Headerless tables require `headerless: true` in your configuration.

    ```yaml
    markdown_extensions:
      - pymdown_multimd_table:
          headerless: true
    ```

A headerless table starts **directly with a separator row** (no header rows
above it). The table has only a `<tbody>` element — no `<thead>`.

## Basic headerless table

[[% set example_1 %]]
| --- | --- |
| No header | here |
| Another   | row  |
[[% endset %]]
[[ table_example(example_1) ]]

## With alignment

Alignment colons work in the separator row just as in regular tables:

[[% set example_2 %]]
| :------- | ---: |
| Left     |  100 |
| Aligned  |   42 |
[[% endset %]]
[[ table_example(example_2) ]]

## With a caption

[[% set example_3 %]]
[Product List]
| --- | --- | --- |
| Widget | blue | $9.99 |
| Gadget | red  | $4.99 |
[[% endset %]]
[[ table_example(example_3) ]]

## Notes

- A separator row **with no following data rows** is not treated as a table.
- With `headerless: false` (the default), a separator-only block is not
  recognised as a table at all.
