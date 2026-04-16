# Inline Formatting

Standard Markdown inline formatting works inside table cells.

## Bold and italic

[[% set example_1 %]]
| Style        | Example               |
| :----------- | :-------------------- |
| Bold         | **bold text**         |
| Italic       | *italic text*         |
| Bold+italic  | ***bold and italic*** |
[[% endset %]]
[[ table_example(example_1) ]]

## Inline code

[[% set example_2 %]]
| Function      | Description                   |
| :------------ | :---------------------------- |
| `help()`      | Display the help window.      |
| `destroy()`   | **Destroy your computer!**    |
| `print(x)`    | Print *x* to stdout.          |
[[% endset %]]
[[ table_example(example_2) ]]

## Links

[[% set example_3 %]]
| Name         | URL                                  |
| :----------- | :----------------------------------- |
| MkDocs       | [mkdocs.org](https://www.mkdocs.org) |
| Material     | [squidfunk.github.io](https://squidfunk.github.io/mkdocs-material) |
[[% endset %]]
[[ table_example(example_3) ]]

## Mixed

[[% set example_4 %]]
| Name          | Signature              | Notes                  |
| :------------ | :--------------------- | :--------------------- |
| `add(a, b)`   | `int, int -> int`      | Returns **sum**        |
| `greet(name)` | `str -> str`           | Returns *greeting*     |
[[% endset %]]
[[ table_example(example_4) ]]
