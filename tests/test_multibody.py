'''Tests for multiple tbody sections separated by blank lines (multibody option).'''

from __future__ import annotations

from tests.conftest import assert_html


class TestMultibody:
    '''multibody=True (default) allows multiple <tbody> sections.'''

    def test_multibody_creates_two_tbody(self):
        src = (
            '| H |\n'
            '| - |\n'
            '| body1 |\n'
            '\n'
            '| body2 |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr><td>body1</td></tr></tbody>'
            '<tbody><tr><td>body2</td></tr></tbody>'
            '</table>',
        )

    def test_multibody_three_sections(self):
        src = (
            '| H |\n'
            '| - |\n'
            '| s1 |\n'
            '\n'
            '| s2 |\n'
            '\n'
            '| s3 |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr><td>s1</td></tr></tbody>'
            '<tbody><tr><td>s2</td></tr></tbody>'
            '<tbody><tr><td>s3</td></tr></tbody>'
            '</table>',
        )

    def test_multibody_single_body_without_blank_line(self):
        src = (
            '| H |\n'
            '| - |\n'
            '| r1 |\n'
            '| r2 |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody>'
            '<tr><td>r1</td></tr>'
            '<tr><td>r2</td></tr>'
            '</tbody></table>',
        )

    def test_multibody_disabled_blank_line_ends_table(self):
        '''With multibody=False, a blank line terminates the table.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| r1 |\n'
            '\n'
            '| r2 |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr><td>r1</td></tr></tbody></table>'
            '<p>| r2 |</p>',
            multibody=False,
        )

    def test_multibody_continuation_stops_at_new_table(self):
        '''A new block with a separator starts a new table, not a new tbody.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| r1 |\n'
            '\n'
            '| H2 |\n'
            '| -- |\n'
            '| r2 |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr><td>r1</td></tr></tbody></table>'
            '<table><thead><tr><th>H2</th></tr></thead>'
            '<tbody><tr><td>r2</td></tr></tbody></table>',
            multibody=True,
        )

    def test_multibody_continuation_stops_at_paragraph(self):
        '''Plain text after a blank line is NOT consumed as a table body.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| row |\n'
            '\n'
            'A plain paragraph.'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr><td>row</td></tr></tbody></table>'
            '<p>A plain paragraph.</p>',
        )
