# Text Alignment

Column alignment is controlled by placing colons (`:`) in the separator row.

| Separator | Alignment |
| :-------: | :-------- |
| `---`     | Default (no alignment style) |
| `:---`    | Left      |
| `:---:`   | Centre    |
| `---:`    | Right     |

## No alignment

```
| A | B |
| - | - |
| 1 | 2 |
```

/// html | div.result
| A | B |
| - | - |
| 1 | 2 |
///

## Left alignment

```
| Item     |
| :------- |
| Apple    |
| Banana   |
```

/// html | div.result
| Item     |
| :------- |
| Apple    |
| Banana   |
///

## Centre alignment

```
| Score  |
| :----: |
| 42     |
| 100    |
```

/// html | div.result
| Score  |
| :----: |
| 42     |
| 100    |
///

## Right alignment

```
| Price  |
| -----: |
| $9.99  |
| $14.99 |
```

/// html | div.result
| Price  |
| -----: |
| $9.99  |
| $14.99 |
///

## Mixed alignment

```
| Item      | Value  | Qty  |
| :-------- | -----: | :--: |
| Computer  | $1600  |  1   |
| Phone     |   $12  |  5   |
| Pipe      |    $1  | 200  |
```

/// html | div.result
| Item      | Value  | Qty  |
| :-------- | -----: | :--: |
| Computer  | $1600  |  1   |
| Phone     |   $12  |  5   |
| Pipe      |    $1  | 200  |
///

!!! note
    Alignment from the separator row applies to **every** body row in the column,
    including the header cell.
