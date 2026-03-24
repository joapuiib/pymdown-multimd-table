'''Tests for column spanning (colspan) via empty cells.'''

from __future__ import annotations

from tests.conftest import assert_html


class TestColspan:
    def test_colspan_two_in_header(self):
        src = (
            '|   | Grouping ||\n'
            '| - | - | - |\n'
            '| A | B | C |'
        )
        assert_html(
            src,
            '<table><thead><tr>'
            '<th></th>'
            '<th colspan="2">Grouping</th>'
            '</tr></thead><tbody>'
            '<tr><td>A</td><td>B</td><td>C</td></tr>'
            '</tbody></table>',
        )

    def test_colspan_in_body(self):
        src = (
            '| A | B | C |\n'
            '| - | - | - |\n'
            '| data      ||\n'
            '| 1 | 2 | 3 |'
        )
        assert_html(
            src,
            '<table><thead><tr>'
            '<th>A</th><th>B</th><th>C</th>'
            '</tr></thead><tbody>'
            '<tr><td colspan=\"2\">data</td></tr>'
            '<tr><td>1</td><td>2</td><td>3</td></tr>'
            '</tbody></table>',
        )

    def test_colspan_three(self):
        '''Three consecutive pipes span three columns.'''
        src = (
            '| A | B | C |\n'
            '| - | - | - |\n'
            '| spans     |||\n'
        )
        assert_html(
            src,
            '<table><thead><tr>'
            '<th>A</th><th>B</th><th>C</th>'
            '</tr></thead><tbody>'
            '<tr><td colspan=\"3\">spans</td></tr>'
            '</tbody></table>',
        )

    def test_colspan_at_row_end(self):
        src = (
            '|   | Grouping ||\n'
            '| - | :-: | -: |\n'
            '| A | *Long*  ||\n'
            '| B | C       | D |'
        )
        assert_html(
            src,
            '<table><thead><tr>'
            '<th></th>'
            '<th colspan="2" style="text-align:center">Grouping</th>'
            '</tr></thead><tbody>'
            '<tr><td>A</td><td colspan="2" style="text-align:center"><em>Long</em></td></tr>'
            '<tr><td>B</td>'
            '<td style="text-align:center">C</td>'
            '<td style="text-align:right">D</td></tr>'
            '</tbody></table>',
        )

    def test_empty_cell_vs_whitespace_cell(self):
        '''Only a strictly empty slice (no chars at all) triggers colspan.
        A cell with only spaces is a real (empty-content) cell.
        '''
        src = (
            '| A  | B  |\n'
            '| -  | -  |\n'
            '| 1  |    |'  # spaces between pipes → real empty cell, not colspan
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th><th>B</th></tr></thead>'
            '<tbody><tr><td>1</td><td></td></tr></tbody></table>',
        )
