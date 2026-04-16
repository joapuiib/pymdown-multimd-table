# Basic Table

The extension supports the standard MultiMarkdown table syntax.
A table requires at least one header row, a separator row made of dashes (`-`),
and one or more body rows.

## Without surrounding pipes

Pipes at the beginning and end of each row are optional.

[[% set without_surrounding_pipes %]]
First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell
[[% endset %]]
[[ table_example(without_surrounding_pipes) ]]

## With surrounding pipes

[[% set with_surrounding_pipes %]]
| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |
[[% endset %]]
[[ table_example(with_surrounding_pipes) ]]

## Single column

[[% set single_column %]]
| Head |
| ---- |
| Data |
| More |
[[% endset %]]
[[ table_example(single_column) ]]

## Escaped pipes

A pipe preceded by a backslash (`\|`) is treated as a literal character,
not a column separator.

[[% set escaped_pipes %]]
| Expression | Result  |
| ---------- | ------- |
| `a \| b`   | a \| b  |
[[% endset %]]
[[ table_example(escaped_pipes) ]]

## Pipe inside a code span

A pipe inside a backtick code span is **not** treated as a column separator.

[[% set pipe_inside_code_span %]]
| Name | Expression |
| ---- | ---------- |
| or   | `a\|b`     |
[[% endset %]]
[[ table_example(pipe_inside_code_span) ]]

## Equal signs in the separator

The separator row also accepts `=` signs instead of `-`.

[[% set equal_sign_separator %]]
First Header  | Second Header
============= | =============
Content Cell  | Content Cell
[[% endset %]]
[[ table_example(equal_sign_separator) ]]
