# pymdown-multimd-table

A **Python-Markdown** extension implementing [MultiMarkdown 6](https://fletcherpenney.net/multimarkdown/) extended table syntax,
mirroring the feature set of the [`markdown-it-multimd-table`](https://github.com/RedBug312/markdown-it-multimd-table) JavaScript plugin.

## Features

### Standard (always enabled)

| Feature | Description |
| :------ | :---------- |
| [Column spanning](syntax/colspan.md) | Empty cells `\|\|` extend the previous cell |
| [Text alignment](syntax/alignment.md) | `:---`, `:---:`, `---:` in the separator row |
| [Wrappable columns](syntax/wrappable.md) | `---+` in the separator adds `class="extend"` |
| [Multiple header rows](syntax/multiple-headers.md) | Multiple rows before the separator |
| [Table captions](syntax/captions.md) | `[caption text]` or `[caption text][label]` |
| [Multiple tbody sections](syntax/multibody.md) | Blank line between data rows |
| [Inline Markdown](syntax/inline-formatting.md) | Bold, italic, code, etc. inside cells |

### Optional (controlled by configuration)

| Option | Default | Description |
| :----- | :-----: | :---------- |
| [`rowspan`](syntax/rowspan.md) | `false` | `^^` in a cell merges it with the cell above |
| [`multiline`](syntax/multiline.md) | `false` | Backslash `\` at end of row continues cell content on the next line |
| [`headerless`](syntax/headerless.md) | `false` | Tables without a header/separator row |
| [`multibody`](syntax/multibody.md) | `true` | Blank lines between data rows create separate `<tbody>` elements |
| [`autolabel`](syntax/captions.md) | `true` | Auto-generate `id` from caption text |
| [`attr_list`](syntax/attr-list.md) | `false` | Parse `{.class #id key=val}` attribute blocks on cells and rows |

## Quick example

```
|              | Grouping      ||
| Header       | A             | B             |
| :----------- | :-----------: | ------------: |
| Row 1        | spans         ||
| Row 2        | left          | right         |
```

/// html | div.result
|              | Grouping      ||
| Header       | A             | B             |
| :----------- | :-----------: | ------------: |
| Row 1        | spans         ||
| Row 2        | left          | right         |
///
