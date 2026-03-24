'''Tests for text alignment in MultiMarkdown tables.'''

from __future__ import annotations

from tests.conftest import assert_html


class TestAlignment:
    def test_center_and_right_alignment(self):
        src = (
            '| Item      | Value |\n'
            '| :-------: | -----:|\n'
            '| Computer  | $1600 |\n'
            '| Phone     |   $12 |'
        )
        assert_html(
            src,
            '<table><thead><tr>'
            '<th style="text-align:center">Item</th>'
            '<th style="text-align:right">Value</th>'
            '</tr></thead><tbody>'
            '<tr><td style="text-align:center">Computer</td>'
            '<td style="text-align:right">$1600</td></tr>'
            '<tr><td style="text-align:center">Phone</td>'
            '<td style="text-align:right">$12</td></tr>'
            '</tbody></table>',
        )

    def test_left_alignment_explicit(self):
        src = (
            '| A |\n'
            '| :- |\n'
            '| 1 |'
        )
        assert_html(
            src,
            '<table><thead><tr>'
            '<th style="text-align:left">A</th>'
            '</tr></thead><tbody>'
            '<tr><td style="text-align:left">1</td></tr>'
            '</tbody></table>',
        )

    def test_no_alignment(self):
        src = (
            '| A |\n'
            '| - |\n'
            '| 1 |'
        )
        assert_html(
            src,
            '<table><thead><tr>'
            '<th>A</th>'
            '</tr></thead><tbody>'
            '<tr><td>1</td></tr>'
            '</tbody></table>',
        )

    def test_equal_signs_in_separator(self):
        '''= signs are valid in the separator row.'''
        src = (
            'First | Second | Third |\n'
            '===== | :=====: | =====:\n'
            'A     | B       | C'
        )
        assert_html(
            src,
            '<table><thead><tr>'
            '<th>First</th>'
            '<th style=\"text-align:center\">Second</th>'
            '<th style=\"text-align:right\">Third</th>'
            '</tr></thead><tbody><tr>'
            '<td>A</td>'
            '<td style=\"text-align:center\">B</td>'
            '<td style=\"text-align:right\">C</td>'
            '</tr></tbody></table>',
        )

    def test_alignment_applied_to_all_body_rows(self):
        '''Alignment from the separator row applies to every body row.'''
        src = (
            '| A | B |\n'
            '| :- | -: |\n'
            '| 1 | 2 |\n'
            '| 3 | 4 |'
        )
        assert_html(
            src,
            '<table><thead><tr>'
            '<th style="text-align:left">A</th>'
            '<th style="text-align:right">B</th>'
            '</tr></thead><tbody>'
            '<tr><td style="text-align:left">1</td>'
            '<td style="text-align:right">2</td></tr>'
            '<tr><td style="text-align:left">3</td>'
            '<td style="text-align:right">4</td></tr>'
            '</tbody></table>',
        )
