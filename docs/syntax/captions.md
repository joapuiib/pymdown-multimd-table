# Table Captions

A caption line can be placed immediately **before** or **after** the table.
The syntax is `[Caption text]` or `[Caption text][label]`.

## Caption before the table

When placed before the table, the caption renders at the **top**.

```
[Sales Data]
| Q1   | Q2   | Q3   | Q4   |
| ---- | ---- | ---- | ---- |
| 100  | 120  | 95   | 140  |
```

/// html | div.result
[Sales Data]
| Q1   | Q2   | Q3   | Q4   |
| ---- | ---- | ---- | ---- |
| 100  | 120  | 95   | 140  |
///

## Caption after the table

When placed after the table, the caption renders at the **bottom**
(using `caption-side: bottom`).

```
| Q1   | Q2   | Q3   | Q4   |
| ---- | ---- | ---- | ---- |
| 100  | 120  | 95   | 140  |
[Annual Sales]
```

/// html | div.result
| Q1   | Q2   | Q3   | Q4   |
| ---- | ---- | ---- | ---- |
| 100  | 120  | 95   | 140  |
[Annual Sales]
///

## Auto-generated ID (autolabel)

When `autolabel` is enabled (default), the caption text is lowercased and
stripped of non-word characters to form the `id` attribute.

```
[Hello, World! 2024]
| A |
| - |
| 1 |
```

/// html | div.result
[Hello, World! 2024]
| A |
| - |
| 1 |
///

The generated `id` attribute will be `helloworld2024`.

## Explicit label

Provide a custom `id` with the `[text][label]` syntax:

```
[My Table][tbl-sales]
| Q1   | Q2   |
| ---- | ---- |
| 100  | 120  |
```

/// html | div.result
[My Table][tbl-sales]
| Q1   | Q2   |
| ---- | ---- |
| 100  | 120  |
///

!!! note "An explicit label **always** overrides the auto-generated one, even when `autolabel` is enabled."

## Disabling autolabel

Set `autolabel: false` in the configuration to suppress automatic ID generation.
Captions without an explicit label will then have no `id` attribute.

```yaml
markdown_extensions:
  - pymdown_multimd_table:
      autolabel: false
```
