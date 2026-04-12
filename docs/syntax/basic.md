# Basic Table

The extension supports the standard MultiMarkdown table syntax.
A table requires at least one header row, a separator row made of dashes (`-`),
and one or more body rows.

## Without surrounding pipes

Pipes at the beginning and end of each row are optional.

```
First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell
```

/// html | div.result
First Header  | Second Header
------------- | -------------
Content Cell  | Content Cell
Content Cell  | Content Cell
///

## With surrounding pipes

```
| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |
```

/// html | div.result
| First Header  | Second Header |
| ------------- | ------------- |
| Content Cell  | Content Cell  |
| Content Cell  | Content Cell  |
///

## Single column

```
| Head |
| ---- |
| Data |
| More |
```

/// html | div.result
| Head |
| ---- |
| Data |
| More |
///

## Escaped pipes

A pipe preceded by a backslash (`\|`) is treated as a literal character,
not a column separator.

```
| Expression | Result  |
| ---------- | ------- |
| `a \| b`   | a \| b  |
```

/// html | div.result
| Expression | Result  |
| ---------- | ------- |
| `a \| b`   | a \| b  |
///

## Pipe inside a code span

A pipe inside a backtick code span is **not** treated as a column separator.

```
| Name | Expression |
| ---- | ---------- |
| or   | `a\|b`     |
```

/// html | div.result
| Name | Expression |
| ---- | ---------- |
| or   | `a\|b`     |
///

## Equal signs in the separator

The separator row also accepts `=` signs instead of `-`.

```
First Header  | Second Header
============= | =============
Content Cell  | Content Cell
```

/// html | div.result
First Header  | Second Header
============= | =============
Content Cell  | Content Cell
///
