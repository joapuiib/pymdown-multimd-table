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

```
| Code           | Output   |
| :------------- | :------- |
| line1          | x       \
| line2          | y       \
| line3          | z        |
```

/// html | div.result
| Code           | Output   |
| :------------- | :------- |
| line1          | x       \
| line2          | y       \
| line3          | z        |
///

## Fenced code block inside a cell

Use the `fenced_code` extension alongside `multiline` to embed code blocks:

```
| Code                    | Result  |
| :---------------------- | :------ |
| ``` python             | hello  |\
| print("hello")         |        |\
| ```                    |         |
```

/// html | div.result
| Code                    | Result  |
| :---------------------- | :------ |
| ``` python             | hello  |\
| print("hello")         |        |\
| ```                    |         |
///

## Bulleted list inside a cell

```
| Steps                   |
| :---------------------- |
| - Install dependencies |\
| - Run `mkdocs serve`   |\
| - Open your browser     |
```

/// html | div.result
| Steps                   |
| :---------------------- |
| - Install dependencies |\
| - Run `mkdocs serve`   |\
| - Open your browser     |
///

## Nested list inside a cell

Relative indentation is preserved, so nested lists work correctly:

```
| Menu                    |
| :---------------------- |
| - Fruit                |\
|     - Apple            |\
|     - Banana           |\
| - Vegetable             |
```

/// html | div.result
| Menu                    |
| :---------------------- |
| - Fruit                |\
|     - Apple            |\
|     - Banana           |\
| - Vegetable             |
///

## Blockquote inside a cell

```
| Quote                    | Author      |
| :----------------------- | :---------- |
| > To be, or not to be,  | Shakespeare |\
| > that is the question. |             |
```

/// html | div.result
| Quote                    | Author      |
| :----------------------- | :---------- |
| > To be, or not to be,  | Shakespeare |\
| > that is the question. |             |
///

## Admonition inside a cell

Requires the [`admonition`](https://python-markdown.github.io/extensions/admonition/)
extension.

```
| Feature       | Notes                        |
| :------------ | :--------------------------- |
| Admonitions   | !!! note                    |\
|               |     Works inside a cell!     |
| Custom title  | !!! warning "Heads up"      |\
|               |     Check your config.       |
```

/// html | div.result
| Feature       | Notes                        |
| :------------ | :--------------------------- |
| Admonitions   | !!! note                    |\
|               |     Works inside a cell!     |
| Custom title  | !!! warning "Heads up"      |\
|               |     Check your config.       |
///

## Definition list inside a cell

Requires the [`def_list`](https://python-markdown.github.io/extensions/definition_lists/)
extension.

```
| Term          | Definition                   |
| :------------ | :--------------------------- |
| Apple         | Apple                       |\
|               | :   A sweet fruit            |
| Python        | Python                      |\
|               | :   A programming language   |
```

/// html | div.result
| Term          | Definition                   |
| :------------ | :--------------------------- |
| Apple         | Apple                       |\
|               | :   A sweet fruit            |
| Python        | Python                      |\
|               | :   A programming language   |
///

## Notes

- Backslash continuation only works in **body** rows. A backslash at the end
  of a header row has no effect.
- With `multiline: false` (the default), a trailing `\` is kept as literal
  cell content.
- Colspan is preserved across continuation lines.
