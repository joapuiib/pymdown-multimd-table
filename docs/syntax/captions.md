# Table Captions

A caption line can be placed immediately **before** or **after** the table.
The syntax is `[Caption text]` or `[Caption text][label]`.

## Caption before the table

When placed before the table, the caption renders at the **top**.

[[% set example_1 %]]
[Sales Data]
| Q1   | Q2   | Q3   | Q4   |
| ---- | ---- | ---- | ---- |
| 100  | 120  | 95   | 140  |
[[% endset %]]
[[ table_example(example_1) ]]

## Caption after the table

When placed after the table, the caption renders at the **bottom**
(using `caption-side: bottom`).

[[% set example_2 %]]
| Q1   | Q2   | Q3   | Q4   |
| ---- | ---- | ---- | ---- |
| 100  | 120  | 95   | 140  |
[Annual Sales]
[[% endset %]]
[[ table_example(example_2) ]]

## Auto-generated ID (autolabel)

When `autolabel` is enabled (default), the caption text is lowercased and
stripped of non-word characters to form the `id` attribute.

[[% set example_3 %]]
[Hello, World! 2024]
| A |
| - |
| 1 |
[[% endset %]]
[[ table_example(example_3) ]]

The generated `id` attribute will be `helloworld2024`.

## Explicit label

Provide a custom `id` with the `[text][label]` syntax:

[[% set example_4 %]]
[My Table][tbl-sales]
| Q1   | Q2   |
| ---- | ---- |
| 100  | 120  |
[[% endset %]]
[[ table_example(example_4) ]]

!!! note "An explicit label **always** overrides the auto-generated one, even when `autolabel` is enabled."

## Disabling autolabel

Set `autolabel: false` in the configuration to suppress automatic ID generation.
Captions without an explicit label will then have no `id` attribute.

```yaml
markdown_extensions:
  - pymdown_multimd_table:
      autolabel: false
```
