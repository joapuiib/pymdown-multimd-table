from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from textwrap import dedent

import markdown
import yaml


CONFIG_PATH = Path(__file__).resolve().parents[2] / "properdocs.yml"


@lru_cache(maxsize=1)
def _markdown_config() -> tuple[list[str], dict[str, object]]:
    config = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))
    extensions: list[str] = []
    extension_configs: dict[str, object] = {}

    for item in config.get("markdown_extensions", []):
        if isinstance(item, str):
            extensions.append(item)
            continue

        for name, options in item.items():
            extensions.append(name)
            if options is not None:
                extension_configs[name] = options

    return extensions, extension_configs


def _normalize_markdown(md_content: str) -> str:
    return dedent(md_content).strip("\n")


def _render_html(md_content: str) -> str:
    extensions, extension_configs = _markdown_config()
    renderer = markdown.Markdown(
        extensions=extensions,
        extension_configs=extension_configs,
    )
    return renderer.convert(md_content)


def define_env(env) -> None:
    @env.macro
    def table_example(md_content: str, result_class: str | None = None) -> str:
        source = _normalize_markdown(md_content)
        html_output = _render_html(source)
        rendered_source = source
        if result_class:
            rendered_source = (
                f'<div class="{result_class}" markdown="1">\n'
                f"{source}\n"
                "</div>"
            )
        return f"""
~~~~md
{source}
~~~~

//// tab | Result

{rendered_source}

////
//// tab | HTML

```html
{html_output}
```

////
"""
