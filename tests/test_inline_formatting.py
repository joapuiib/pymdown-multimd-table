'''Tests for inline Markdown formatting inside table cells.'''

from __future__ import annotations

from tests.conftest import assert_html


class TestInlineFormatting:
    def test_bold_in_cell(self):
        src = (
            '| A |\n'
            '| - |\n'
            '| **bold** |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th></tr></thead><tbody>'
            '<tr><td><strong>bold</strong></td></tr>'
            '</tbody></table>',
        )

    def test_italic_in_cell(self):
        src = (
            '| A |\n'
            '| - |\n'
            '| *italic* |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th></tr></thead><tbody>'
            '<tr><td><em>italic</em></td></tr>'
            '</tbody></table>',
        )

    def test_code_in_cell(self):
        src = (
            '| A |\n'
            '| - |\n'
            '| `code()` |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th></tr></thead><tbody>'
            '<tr><td><code>code()</code></td></tr>'
            '</tbody></table>',
        )

    def test_mixed_inline(self):
        src = (
            '| Function name | Description               |\n'
            '| ------------- | ------------------------- |\n'
            '| `help()`      | Display the help window.  |\n'
            '| `destroy()`   | **Destroy your computer!**|'
        )
        assert_html(
            src,
            '<table><thead><tr>'
            '<th>Function name</th><th>Description</th>'
            '</tr></thead><tbody><tr>'
            '<td><code>help()</code></td><td>Display the help window.</td></tr><tr>'
            '<td><code>destroy()</code></td><td><strong>Destroy your computer!</strong></td></tr>'
            '</tbody></table>',
        )
