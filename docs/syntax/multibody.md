# Multiple Bodies

When `multibody` is enabled (the default), a **blank line** between data rows
starts a new `<tbody>` section. This is useful for visually and semantically
grouping rows.

## Basic example

[[% set example_1 %]]
| Category  | Item    | Price  |
| :-------- | :------ | -----: |
| Fruit     | Apple   | $0.50  |
| Fruit     | Banana  | $0.30  |

| Vegetable | Carrot  | $0.80  |
| Vegetable | Onion   | $0.60  |
[[% endset %]]
[[ table_example(example_1) ]]

## Three sections

[[% set example_2 %]]
| H |
| - |
| Section 1 row A |
| Section 1 row B |

| Section 2 row A |

| Section 3 row A |
| Section 3 row B |
| Section 3 row C |
[[% endset %]]
[[ table_example(example_2) ]]

## Disabling multibody

With `multibody: false`, a blank line **ends** the table. Any subsequent rows
are parsed as a new paragraph.

```yaml
markdown_extensions:
  - pymdown_multimd_table:
      multibody: false
```

!!! note
    A blank line followed by a **new table** (with its own separator row)
    always starts a new `<table>` element, regardless of the `multibody` setting.
