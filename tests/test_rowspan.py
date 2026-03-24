'''Tests for row spanning via the ^^ syntax (rowspan option).'''

from __future__ import annotations

from tests.conftest import convert, assert_html


class TestRowspan:
    '''rowspan=True enables ^^ to merge a cell with the one above.'''

    def test_simple_rowspan(self):
        src = (
            '| A | B |\n'
            '| - | - |\n'
            '| X | Y |\n'
            '| ^^ | Z |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th><th>B</th></tr></thead>'
            '<tbody>'
            '<tr><td rowspan="2">X</td><td>Y</td></tr>'
            '<tr><td>Z</td></tr>'
            '</tbody></table>',
            rowspan=True,
        )

    def test_rowspan_three_rows(self):
        src = (
            '| A | B |\n'
            '| - | - |\n'
            '| X | 1 |\n'
            '| ^^ | 2 |\n'
            '| ^^ | 3 |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th><th>B</th></tr></thead>'
            '<tbody>'
            '<tr><td rowspan="3">X</td><td>1</td></tr>'
            '<tr><td>2</td></tr>'
            '<tr><td>3</td></tr>'
            '</tbody></table>',
            rowspan=True,
        )

    def test_rowspan_and_colspan_combined(self):
        src = (
            '| A || |\n'
            '| --- | --- | --- |\n'
            '| B  | C  | D  |\n'
            '| ^^ | E  | F  |\n'
            '| G  || H  |\n'
            '| ^^ || I  |\n'
            '| ^^ || J  |'
        )
        assert_html(
            src,
            '<table><thead><tr>'
            '<th colspan="2">A</th><th></th>'
            '</tr></thead><tbody>'
            '<tr><td rowspan="2">B</td><td>C</td><td>D</td></tr>'
            '<tr><td>E</td><td>F</td></tr>'
            '<tr><td colspan="2" rowspan="3">G</td><td>H</td></tr>'
            '<tr><td>I</td></tr>'
            '<tr><td>J</td></tr>'
            '</tbody></table>',
            rowspan=True,
        )

    def test_rowspan_in_header_is_literal(self):
        '''^^ in a header row is treated as literal text, not rowspan.'''
        src = (
            '| ^^ | A | B |\n'
            '| -- | - | - |\n'
            '| ^^ | C | D |\n'
            '| ^^ | E | F |'
        )
        assert_html(
            src,
            '<table><thead><tr>'
            '<th>^^</th><th>A</th><th>B</th>'
            '</tr></thead><tbody>'
            '<tr><td rowspan="2">^^</td><td>C</td><td>D</td></tr>'
            '<tr><td>E</td><td>F</td></tr>'
            '</tbody></table>',
            rowspan=True,
        )

    def test_rowspan_disabled_caret_is_literal(self):
        '''With rowspan=False (default), ^^ renders as literal cell content.'''
        src = (
            '| A | B |\n'
            '| - | - |\n'
            '| X | Y |\n'
            '| ^^ | Z |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th><th>B</th></tr></thead>'
            '<tbody>'
            '<tr><td>X</td><td>Y</td></tr>'
            '<tr><td>^^</td><td>Z</td></tr>'
            '</tbody></table>',
        )

    def test_rowspan_colspan_base_case(self):
        '''Rowspan and colspan can combine on the same cell.'''
        src = (
            '|    |    |    |\n'
            '|----|----|----|  \n'
            '| A  | B      ||\n'
            '| C  | ^^     ||'
        )
        assert_html(
            src,
            '<table><thead><tr><th></th><th></th><th></th></tr></thead>'
            '<tbody>'
            '<tr><td>A</td><td colspan="2" rowspan="2">B</td></tr>'
            '<tr><td>C</td></tr>'
            '</tbody></table>',
            rowspan=True,
        )
