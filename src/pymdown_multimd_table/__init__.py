"""Python-Markdown extension for MultiMarkdown 6 table syntax.

Mimics the markdown-it-multimd-table JavaScript plugin, adding:
- Column spanning (colspan) with empty cells (``||``)
- Row spanning (rowspan) with ``^^`` syntax
- Text alignment via colon markers in separator
- Multiple header rows
- Table captions with optional labels
- Multiple tbody sections separated by blank lines
- Multiline cells with backslash continuation
- Headerless tables
- Wrappable columns with ``+`` suffix in separator
"""

from .extension import MultimdTableExtension, makeExtension

__all__ = ["MultimdTableExtension", "makeExtension"]
