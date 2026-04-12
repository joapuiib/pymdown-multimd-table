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

```
| A      | B  | C  |
| :----- | :- | :- |
| tall   | 1  | x  |
| ^^     | 2  | y  |
```

/// html | div.result
| A      | B  | C  |
| :----- | :- | :- |
| tall   | 1  | x  |
| ^^     | 2  | y  |
///

## Three-row span

```
| A      | B  |
| :----- | :- |
| big    | 1  |
| ^^     | 2  |
| ^^     | 3  |
```

/// html | div.result
| A      | B  |
| :----- | :- |
| big    | 1  |
| ^^     | 2  |
| ^^     | 3  |
///

## Rowspan and colspan combined

```
| A ||  |
| --- | --- | --- |
| B  | C  | D  |
| ^^ | E  | F  |
| G  || H  |
| ^^ || I  |
| ^^ || J  |
```

/// html | div.result
| A ||  |
| --- | --- | --- |
| B  | C  | D  |
| ^^ | E  | F  |
| G  || H  |
| ^^ || I  |
| ^^ || J  |
///

## Notes

- `^^` is only recognised in **body** rows. In a header row it is treated as
  literal text.
- With `rowspan: false` (the default), `^^` is rendered as literal cell content.
