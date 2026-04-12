# Attribute Lists

!!! info "Optional feature"
    Attribute lists require `attr_list: true` in your configuration.

    ```yaml
    markdown_extensions:
      - pymdown_multimd_table:
          attr_list: true
    ```

<style>
  .attr-list-demo td.featured,
  .attr-list-demo th.featured {
    background: color-mix(in srgb, var(--md-primary-fg-color) 12%, transparent);
    box-shadow: inset 4px 0 0 var(--md-primary-fg-color);
    font-weight: 700;
  }

  .attr-list-demo #sale-price {
    color: var(--md-accent-fg-color);
    font-weight: 700;
  }

  .attr-list-demo tr.featured-row > * {
    background: color-mix(in srgb, var(--md-accent-fg-color) 10%, transparent);
  }

  .attr-list-demo tr.featured-row > :first-child {
    box-shadow: inset 4px 0 0 var(--md-accent-fg-color);
  }

  .attr-list-demo thead tr.featured-row > * {
    background: color-mix(in srgb, var(--md-primary-fg-color) 14%, transparent);
  }

  .attr-list-demo tbody.bg-color-green td {
    background: rgba(76, 175, 80, 0.12);
  }

  .attr-list-demo tbody.bg-color-orange td {
    background: rgba(255, 152, 0, 0.12);
  }

  .attr-list-demo table.bg-color-primary {
    border: 2px solid var(--md-primary-fg-color);
    border-radius: 0.2rem;
  }

  .attr-list-demo table.bg-color-primary th {
    background: color-mix(in srgb, var(--md-primary-fg-color) 10%, transparent);
  }

  .attr-list-demo td.extend.wrap,
  .attr-list-demo th.extend.wrap {
    background: color-mix(in srgb, var(--md-accent-fg-color) 10%, transparent);
    white-space: normal;
    word-break: break-word;
  }
</style>

Attribute lists let you attach HTML attributes directly to table elements. For styling,
the most useful token is usually `.class`, but `#id` and `key="value"` work too.

| Token | Common use |
| :---- | :--------- |
| `.class` | Add a reusable CSS hook |
| `#id` | Target one specific element |
| `key="value"` | Add any other HTML attribute such as `data-*` |

## Where the attributes go

| Placement | Target element | Example |
| :-------- | :------------- | :------ |
| Inside a cell, before the closing `|` | `<td>` or `<th>` | `Sale {.featured}` |
| After the last `|` in a row | `<tr>` | `| 19 |{.featured-row}` |
| Standalone `{...}` line after a body section | `<tbody>` | `{.bg-color-green}` |
| Final standalone `{...}` line in the table block | `<table>` | `{.bg-color-primary}` |

## Style a single cell

Put the attribute block inside the cell. The class lands on the rendered `<td>`.

```markdown
| Item | Price |
| :--- | ----: |
| Notebook {.featured} | $12 |
| Pencil | $2 {#sale-price} |
```

<div class="result attr-list-demo" markdown="1">
| Item | Price |
| :--- | ----: |
| Notebook {.featured} | $12 |
| Pencil | $2 {#sale-price} |
</div>

```html
<td class="featured">Notebook</td>
<td id="sale-price">$2</td>
```

## Style header cells

The same syntax works in the header row, so the attributes land on `<th>`.

```markdown
| Plan {.featured} | Seats |
| :------------------- | ----: |
| Starter | 3 |
| Pro | 10 |
```

<div class="result attr-list-demo" markdown="1">
| Plan {.featured} | Seats |
| :------------------- | ----: |
| Starter | 3 |
| Pro | 10 |
</div>

```html
<th class="featured">Plan</th>
```

## Style a full row

Put the attribute block after the last pipe. The class is applied to the `<tr>`,
so every cell in that row picks up the styling.

```markdown
| Plan | Price |
| :--- | ----: |
| Starter | $9 |
| Pro | $29 |{.featured-row}
```

<div class="result attr-list-demo" markdown="1">
| Plan | Price |
| :--- | ----: |
| Starter | $9 |
| Pro | $29 |{.featured-row}
</div>

```html
<tr class="featured-row">
  <td>Pro</td>
  <td>$29</td>
</tr>
```

## Style a header row

Row attributes also work on header rows.

```markdown
| Name | Role |{.featured-row}
| :---------------- | :--- |
| Ana | Maintainer |
```

<div class="result attr-list-demo" markdown="1">
| Name | Role |{.featured-row}
| :---------------- | :--- |
| Ana | Maintainer |
</div>

```html
<thead>
  <tr class="featured-row">
    <th>Name</th>
    <th>Role</th>
  </tr>
</thead>
```

## Style a tbody section

With `multibody: true`, a standalone `{...}` line after a body section applies to
that `<tbody>`. Because the final standalone attribute line is always table-level,
the last body in this example gets its own class and the table gets one too.

```markdown
| Category | Item |
| :------- | :--- |
| Fruit | Apple |
| Fruit | Banana |
{.bg-color-green}

| Vegetable | Carrot |
| Vegetable | Onion |
{.bg-color-orange}
{.bg-color-primary}
```

<div class="result attr-list-demo" markdown="1">
| Category | Item |
| :------- | :--- |
| Fruit | Apple |
| Fruit | Banana |
{.bg-color-green}

| Vegetable | Carrot |
| Vegetable | Onion |
{.bg-color-orange}
{.bg-color-primary}
</div>

```html
<table class="bg-color-primary">
    <tbody class="bg-color-green">...</tbody>
    <tbody class="bg-color-orange">...</tbody>
</table>
```

!!! tip "Requires multibody"
    Tbody attributes are only meaningful when `multibody: true` is enabled.

## Style the whole table

The last standalone `{...}` line in the table block always targets the `<table>`
element itself.

```markdown
| Item | Stock |
| :--- | ----: |
| Notebook | 18 |
| Pencil | 41 |
{.bg-color-primary}
```

<div class="result attr-list-demo" markdown="1">
| Item | Stock |
| :--- | ----: |
| Notebook | 18 |
| Pencil | 41 |
{.bg-color-primary}
</div>

```html
<table class="bg-color-primary">...</table>
```

If you need attributes on both the last `<tbody>` and the `<table>`, use two
consecutive lines at the end:

```markdown
| Item |
| :--- |
| Notebook |
{.bg-color-green}
{.bg-color-primary}
```

## Combine classes with other table features

Attribute lists are preserved when other table features are active.

### Wrappable columns

Your class is appended to the built-in `extend` class.

```markdown
| Name | Notes {.wrap} |
| :--- | :----------------------+ |
| Pencil | Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua {.wrap} |
```

<div class="result attr-list-demo" markdown="1">
| Name | Notes {.wrap} |
| :--- | :----------------------+ |
| Pencil | Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua {.wrap} |
</div>

```html
<th class="extend wrap">Notes</th>
<td class="extend wrap">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua</td>
```

### Alignment, colspan, and rowspan

- Alignment styles stay on the same element as your class.
- Colspan and rowspan preserve your attributes on the merged cell.
- Cell and row attributes can be used together on the same row.

## Disabled by default

When `attr_list: false` is left at its default value, `{...}` is not consumed as
table metadata:

- Inside a cell, it stays as literal text.
- After the last `|`, it becomes another cell.
- On a standalone line, it is not treated as a table attribute.

!!! tip
    The `attr_list` option is compatible with the standard
    [`attr_list`](https://python-markdown.github.io/extensions/attr_list/)
    Markdown extension, so you can enable both:

    ```yaml
    markdown_extensions:
      - pymdown_multimd_table:
          attr_list: true
      - attr_list
    ```
