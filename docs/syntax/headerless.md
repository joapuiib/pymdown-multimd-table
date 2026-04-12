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

```
| --- | --- |
| No header | here |
| Another   | row  |
```

/// html | div.result
| --- | --- |
| No header | here |
| Another   | row  |
///

## With alignment

Alignment colons work in the separator row just as in regular tables:

```
| :------- | ---: |
| Left     |  100 |
| Aligned  |   42 |
```

/// html | div.result
| :------- | ---: |
| Left     |  100 |
| Aligned  |   42 |
///

## With a caption

```
[Product List]
| --- | --- | --- |
| Widget | blue | $9.99 |
| Gadget | red  | $4.99 |
```

/// html | div.result
[Product List]
| --- | --- | --- |
| Widget | blue | $9.99 |
| Gadget | red  | $4.99 |
///

## Notes

- A separator row **with no following data rows** is not treated as a table.
- With `headerless: false` (the default), a separator-only block is not
  recognised as a table at all.
