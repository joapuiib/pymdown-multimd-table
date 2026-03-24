'''Tests for basic MultiMarkdown table structure.'''

from __future__ import annotations

from tests.conftest import convert, assert_html


class TestBasicStructure:
    def test_without_leading_trailing_pipes(self):
        src = (
            'First Header  | Second Header\n'
            '------------- | -------------\n'
            'Content Cell  | Content Cell\n'
            'Content Cell  | Content Cell'
        )
        assert_html(
            src,
            '<table><thead><tr>'
            '<th>First Header</th><th>Second Header</th>'
            '</tr></thead><tbody>'
            '<tr><td>Content Cell</td><td>Content Cell</td></tr>'
            '<tr><td>Content Cell</td><td>Content Cell</td></tr>'
            '</tbody></table>',
        )

    def test_with_leading_and_trailing_pipes(self):
        src = (
            '| First Header  | Second Header |\n'
            '| ------------- | ------------- |\n'
            '| Content Cell  | Content Cell  |\n'
            '| Content Cell  | Content Cell  |'
        )
        assert_html(
            src,
            '<table><thead><tr>'
            '<th>First Header</th><th>Second Header</th>'
            '</tr></thead><tbody>'
            '<tr><td>Content Cell</td><td>Content Cell</td></tr>'
            '<tr><td>Content Cell</td><td>Content Cell</td></tr>'
            '</tbody></table>',
        )

    def test_single_column(self):
        src = (
            '| Head |\n'
            '| ---- |\n'
            '| Data |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>Head</th></tr></thead>'
            '<tbody><tr><td>Data</td></tr></tbody></table>',
        )

    def test_not_a_table_missing_separator(self):
        src = (
            '| A | B |\n'
            '| 1 | 2 |'
        )
        result = convert(src)
        assert '<table>' not in result

    def test_not_a_table_too_short(self):
        src = '| A | B |'
        result = convert(src)
        assert '<table>' not in result

    def test_invalid_separator_character(self):
        '''A * in the separator row makes it invalid.'''
        src = (
            '| A | B | C |\n'
            '| - | - | -* |\n'
            '| 1 | 2 | 3 |'
        )
        result = convert(src)
        assert '<table>' not in result

    def test_escaped_pipes_are_not_column_separators(self):
        r'''\\| inside a cell is literal, not a column separator.'''
        src = (
            'First | Second | Third |\n'
            '----- | :----: | -----:\n'
            r'A \| B | C | D |'
        )
        assert_html(
            src,
            '<table><thead><tr>'
            '<th>First</th>'
            '<th style="text-align:center">Second</th>'
            '<th style="text-align:right">Third</th>'
            '</tr></thead><tbody><tr>'
            '<td>A | B</td>'
            '<td style="text-align:center">C</td>'
            '<td style="text-align:right">D</td>'
            '</tr></tbody></table>',
        )

    def test_pipe_inside_backtick_code_not_a_separator(self):
        '''A pipe inside a backtick code span is not a column separator.'''
        src = (
            '| Name | Expr |\n'
            '| ---- | ---- |\n'
            '| x    | `a|b` |'
        )
        assert_html(
            src,
            '<table><thead><tr>'
            '<th>Name</th><th>Expr</th>'
            '</tr></thead><tbody><tr>'
            '<td>x</td><td><code>a|b</code></td>'
            '</tr></tbody></table>',
        )
