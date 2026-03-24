'''Tests for edge cases and non-table content handling.'''

from __future__ import annotations

from tests.conftest import convert, assert_html


class TestEdgeCases:
    def test_table_does_not_consume_following_paragraph(self):
        src = (
            '| A |\n'
            '| - |\n'
            '| 1 |\n'
            '\n'
            'Normal paragraph.'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th></tr></thead>'
            '<tbody><tr><td>1</td></tr></tbody></table>'
            '<p>Normal paragraph.</p>',
        )

    def test_paragraph_before_table(self):
        src = (
            'A paragraph.\n'
            '\n'
            '| A |\n'
            '| - |\n'
            '| 1 |'
        )
        assert_html(
            src,
            '<p>A paragraph.</p>'
            '<table><thead><tr><th>A</th></tr></thead>'
            '<tbody><tr><td>1</td></tr></tbody></table>',
        )

    def test_indented_four_spaces_is_code_block_not_table(self):
        '''A separator line indented by 4+ spaces is treated as a code block.'''
        src = (
            '| A | B |\n'
            '    | - | - |\n'
            '| 1 | 2 |'
        )
        result = convert(src)
        assert '<table>' not in result

    def test_extra_columns_in_body_are_rendered(self):
        '''Body rows may have more columns than the separator; extras get no alignment.'''
        src = (
            '| A | B |\n'
            '| - | - |\n'
            '| 1 | 2 | EXTRA |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th><th>B</th></tr></thead>'
            '<tbody><tr><td>1</td><td>2</td><td>EXTRA</td></tr></tbody></table>',
        )

    def test_body_row_with_fewer_columns_than_separator(self):
        '''A body row with fewer columns than the separator is valid.'''
        src = (
            '| A | B | C |\n'
            '| - | - | - |\n'
            '| 1 |'           # only 1 column
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th><th>B</th><th>C</th></tr></thead>'
            '<tbody><tr><td>1</td></tr></tbody></table>',
        )
