# Configuration

## In MkDocs

Add the extension to your `mkdocs.yml`:

```yaml
markdown_extensions:
  - pymdown_multimd_table
```

With options:

```yaml
markdown_extensions:
  - pymdown_multimd_table:
      rowspan: true
      multiline: true
      headerless: true
      multibody: true    # default
      autolabel: true    # default
      attr_list: true
```

## In Python

```python
import markdown

md = markdown.Markdown(extensions=["pymdown_multimd_table"])
html = md.convert(source)
```

With options:

```python
md = markdown.Markdown(
    extensions=["pymdown_multimd_table"],
    extension_configs={
        "pymdown_multimd_table": {
            "rowspan": True,
            "multiline": True,
            "headerless": True,
            "multibody": True,   # default
            "autolabel": True,   # default
            "attr_list": True,
        }
    },
)
```

## Options reference

| Option | Type | Default | Description |
| :----- | :--: | :-----: | :---------- |
| `rowspan` | bool | `false` | Enable `^^` row-spanning syntax |
| `multiline` | bool | `false` | Enable `\` line-continuation for multi-line cells |
| `headerless` | bool | `false` | Allow tables that start directly with a separator row (no header) |
| `multibody` | bool | `true` | A blank line between data rows creates a new `<tbody>` element |
| `autolabel` | bool | `true` | Derive an `id` from the caption text when no explicit label is given |
| `attr_list` | bool | `false` | Parse `{.class #id key=val}` attribute blocks on cells and rows |
