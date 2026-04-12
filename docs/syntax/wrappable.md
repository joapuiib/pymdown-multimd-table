# Wrappable Columns

Adding `+` at the end of a separator cell marks that column as *wrappable*.
The extension adds `class="extend"` to every `<th>` and `<td>` in that column,
which you can then style with CSS to allow text to wrap.

## Basic example

```
| Name        | Description                                 | Tags  |
| :---------- | :-----------------------------------------+ | :---- |
| Lorem Ipsum | A long description that should be wrappable | docs  |
| Short       | Brief                                       | misc  |
```

/// html | div.result
| Name        | Description                                 | Tags  |
| :---------- | :-----------------------------------------+ | :---- |
| Lorem Ipsum | A long description that should be wrappable | docs  |
| Short       | Brief                                       | misc  |
///

## Wrappable with alignment

The `+` marker can be combined with alignment colons:

| Separator   | Effect                       |
| :---------- | :--------------------------- |
| `-+`        | Wrappable, no alignment      |
| `:-+`       | Wrappable, left-aligned      |
| `:-:+`      | Wrappable, centre-aligned    |
| `-:+`       | Wrappable, right-aligned     |

```
| Col A    | Col B (centred + wrappable)         | Col C  |
| :------- | :---------------------------------:+ | -----: |
| value    | This cell wraps and is centred      | 42     |
```

/// html | div.result
| Col A    | Col B (centred + wrappable)         | Col C  |
| :------- | :---------------------------------:+ | -----: |
| value    | This cell wraps and is centred      | 42     |
///

!!! tip "Styling wrappable columns"
    The `extend` class does not add any default style. Add a rule such as the
    following to your stylesheet to enable wrapping:

    ```css
    td.extend, th.extend {
      white-space: normal;
      word-break: break-word;
    }
    ```
