'''Tests for combinations of multiple optional features.'''

from __future__ import annotations

from tests.conftest import assert_html


class TestCombinations:
    def test_rowspan_with_multibody(self):
        src = (
            '| H1 | H2 |\n'
            '| -- | -- |\n'
            '| A  | 1  |\n'
            '| ^^ | 2  |\n\n'
            '| B  | 3  |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H1</th><th>H2</th></tr></thead>'
            '<tbody>'
            '<tr><td rowspan="2">A</td><td>1</td></tr>'
            '<tr><td>2</td></tr>'
            '</tbody>'
            '<tbody><tr><td>B</td><td>3</td></tr></tbody>'
            '</table>',
            rowspan=True,
        )

    def test_colspan_with_alignment(self):
        src = (
            '|   | Group ||\n'
            '| - | :-:   | -: |\n'
            '| A | span  ||\n'
        )
        assert_html(
            src,
            '<table><thead><tr>'
            '<th></th>'
            '<th colspan="2" style="text-align:center">Group</th>'
            '</tr></thead><tbody><tr>'
            '<td>A</td>'
            '<td colspan="2" style="text-align:center">span</td>'
            '</tr></tbody></table>',
        )

    def test_caption_with_headerless(self):
        src = (
            '[Data]\n'
            '| - |\n'
            '| 1 |'
        )
        assert_html(
            src,
            '<table><caption id="data">Data</caption>'
            '<tbody><tr><td>1</td></tr></tbody></table>',
            headerless=True,
        )

    def test_multiline_with_rowspan(self):
        '''Multiline merging takes priority: ^^ inside a merged row is content.'''
        src = (
            '| A | B |\n'
            '| - | - |\n'
            '| X | Y |\\\n'
            '| ^^ | Z |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th><th>B</th></tr></thead>'
            '<tbody><tr>'
            '<td><p>X ^^</p></td>'
            '<td><p>Y Z</p></td>'
            '</tr></tbody></table>',
            multiline=True,
            rowspan=True,
        )
