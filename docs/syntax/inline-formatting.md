# Inline Formatting

Standard Markdown inline formatting works inside table cells.

## Bold and italic

```
| Style        | Example               |
| :----------- | :-------------------- |
| Bold         | **bold text**         |
| Italic       | *italic text*         |
| Bold+italic  | ***bold and italic*** |
```

/// html | div.result
| Style        | Example               |
| :----------- | :-------------------- |
| Bold         | **bold text**         |
| Italic       | *italic text*         |
| Bold+italic  | ***bold and italic*** |
///

## Inline code

```
| Function      | Description                   |
| :------------ | :---------------------------- |
| `help()`      | Display the help window.      |
| `destroy()`   | **Destroy your computer!**    |
| `print(x)`    | Print *x* to stdout.          |
```

/// html | div.result
| Function      | Description                   |
| :------------ | :---------------------------- |
| `help()`      | Display the help window.      |
| `destroy()`   | **Destroy your computer!**    |
| `print(x)`    | Print *x* to stdout.          |
///

## Links

```
| Name         | URL                                  |
| :----------- | :----------------------------------- |
| MkDocs       | [mkdocs.org](https://www.mkdocs.org) |
| Material     | [squidfunk.github.io](https://squidfunk.github.io/mkdocs-material) |
```

/// html | div.result
| Name         | URL                                  |
| :----------- | :----------------------------------- |
| MkDocs       | [mkdocs.org](https://www.mkdocs.org) |
| Material     | [squidfunk.github.io](https://squidfunk.github.io/mkdocs-material) |
///

## Mixed

```
| Name          | Signature              | Notes                  |
| :------------ | :--------------------- | :--------------------- |
| `add(a, b)`   | `int, int -> int`      | Returns **sum**        |
| `greet(name)` | `str -> str`           | Returns *greeting*     |
```

/// html | div.result
| Name          | Signature              | Notes                  |
| :------------ | :--------------------- | :--------------------- |
| `add(a, b)`   | `int, int -> int`      | Returns **sum**        |
| `greet(name)` | `str -> str`           | Returns *greeting*     |
///
