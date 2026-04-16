# Multiline Cells

!!! info "Optional feature"
    Multiline cells require `multiline: true` in your configuration.

    ```yaml
    markdown_extensions:
      - pymdown_multimd_table:
          multiline: true
    ```

End a row with a backslash `\` to continue the current cell content on the
next line. The lines are joined into a single cell and parsed as a block of
Markdown.

## Basic multiline

[[% set example_1 %]]
| Code           | Output   |
| :------------- | :------- |
| line1          | x       \
| line2          | y       \
| line3          | z        |
[[% endset %]]
[[ table_example(example_1) ]]

## Fenced code block inside a cell

Use the `fenced_code` extension alongside `multiline` to embed code blocks:

[[% set example_2 %]]
| Code                    | Result  |
| :---------------------- | :------ |
| ``` python             | hello  |\
| print("hello")         |        |\
| ```                    |         |
[[% endset %]]
[[ table_example(example_2) ]]

## Bulleted list inside a cell

[[% set example_3 %]]
| Steps                   |
| :---------------------- |
| - Install dependencies |\
| - Run `mkdocs serve`   |\
| - Open your browser     |
[[% endset %]]
[[ table_example(example_3) ]]

## Nested list inside a cell

Relative indentation is preserved, so nested lists work correctly:

[[% set example_4 %]]
| Menu                    |
| :---------------------- |
| - Fruit                |\
|     - Apple            |\
|     - Banana           |\
| - Vegetable             |
[[% endset %]]
[[ table_example(example_4) ]]

## Blockquote inside a cell

[[% set example_5 %]]
| Quote                    | Author      |
| :----------------------- | :---------- |
| > To be, or not to be,  | Shakespeare |\
| > that is the question. |             |
[[% endset %]]
[[ table_example(example_5) ]]

## Admonition inside a cell

Requires the [`admonition`](https://python-markdown.github.io/extensions/admonition/)
extension.

[[% set example_6 %]]
| Feature       | Notes                        |
| :------------ | :--------------------------- |
| Admonitions   | !!! note                    |\
|               |     Works inside a cell!     |
| Custom title  | !!! warning "Heads up"      |\
|               |     Check your config.       |
[[% endset %]]
[[ table_example(example_6) ]]

## Definition list inside a cell

Requires the [`def_list`](https://python-markdown.github.io/extensions/definition_lists/)
extension.

[[% set example_7 %]]
| Term          | Definition                   |
| :------------ | :--------------------------- |
| Apple         | Apple                       |\
|               | :   A sweet fruit            |
| Python        | Python                      |\
|               | :   A programming language   |
[[% endset %]]
[[ table_example(example_7) ]]

## Notes

- Backslash continuation only works in **body** rows. A backslash at the end
  of a header row has no effect.
- With `multiline: false` (the default), a trailing `\` is kept as literal
  cell content.
- Colspan is preserved across continuation lines.
