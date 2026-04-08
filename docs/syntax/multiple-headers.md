# Multiple Header Rows

You can add multiple header rows by placing more than one row **before** the
separator line. All rows above the first separator become `<th>` cells inside
`<thead>`.

## Two header rows

```
| Group 1  | Group 2  |
| A        | B        |
| -------- | -------- |
| 1        | 2        |
```

/// html | div.result
| Group 1  | Group 2  |
| A        | B        |
| -------- | -------- |
| 1        | 2        |
///

## Three header rows

```
| Level 1A | Level 1B |
| Level 2A | Level 2B |
| Level 3A | Level 3B |
| --------- | --------- |
| data      | data      |
```

/// html | div.result
| Level 1A | Level 1B |
| Level 2A | Level 2B |
| Level 3A | Level 3B |
| --------- | --------- |
| data      | data      |
///

## Combined with column spanning

Multiple header rows pair naturally with column spanning to build rich
hierarchical headers.

```
|              | Q1           || Q2           ||
|              | Jan  | Feb   | Mar  | Apr    |
| :----------- | ---: | ----: | ---: | -----: |
| Product A    | 100  | 120   | 90   | 130    |
| Product B    | 200  | 180   | 210  | 195    |
```

/// html | div.result
|              | Q1           || Q2           ||
|              | Jan  | Feb   | Mar  | Apr    |
| :----------- | ---: | ----: | ---: | -----: |
| Product A    | 100  | 120   | 90   | 130    |
| Product B    | 200  | 180   | 210  | 195    |
///
