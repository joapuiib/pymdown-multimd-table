'''Tests for wrappable columns (--- + marker adds class="extend").'''

from __future__ import annotations

from tests.conftest import assert_html


class TestWrappable:
    def test_wrappable_adds_extend_class(self):
        src = (
            '| A | B | C |\n'
            '| - | -+ | - |\n'
            '| 1 | 2 | 3 |'
        )
        assert_html(
            src,
            '<table><thead><tr>'
            '<th>A</th>'
            '<th class="extend">B</th>'
            '<th>C</th>'
            '</tr></thead><tbody>'
            '<tr><td>1</td><td class=\"extend\">2</td><td>3</td></tr>'
            '</tbody></table>',
        )

    def test_wrappable_with_alignment(self):
        # No space before '+' — the wrappable marker follows colon directly.
        src = (
            '| A  | B   |\n'
            '| -- | :-:+ |\n'
            '| 1  | 2   |'
        )
        assert_html(
            src,
            '<table><thead><tr>'
            '<th>A</th>'
            '<th class="extend" style="text-align:center">B</th>'
            '</tr></thead><tbody>'
            '<tr><td>1</td><td class=\"extend\" style=\"text-align:center\">2</td></tr>'
            '</tbody></table>',
        )

    def test_non_wrappable_no_extend_class(self):
        src = (
            '| A | B |\n'
            '| - | - |\n'
            '| 1 | 2 |'
        )
        assert_html(
            src,
            '<table><thead><tr>'
            '<th>A</th><th>B</th>'
            '</tr></thead><tbody><tr>'
            '<td>1</td><td>2</td>'
            '</tr></tbody></table>',
        )
