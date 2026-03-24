'''Tests for multiline cells via backslash continuation (multiline option).'''

from __future__ import annotations

from tests.conftest import assert_html


class TestMultiline:
    '''multiline=True allows backslash at end of row to continue to next row.'''

    def test_multiline_creates_block_content(self):
        '''Backslash continuation merges rows into a single cell.'''
        src = (
            'A         | B\n'
            '----------|---------\n'
            'line1     | x      \\\n'
            'line2     | y      \\\n'
            'line3     |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th><th>B</th></tr></thead>'
            '<tbody><tr>'
            '<td><p>line1 line2 line3</p></td>'
            '<td><p>x y</p></td>'
            '</tr></tbody></table>',
            multiline=True,
        )

    def test_multiline_trailing_pipe(self):
        '''Backslash can appear after a trailing pipe.'''
        src = (
            'A         | B     |\n'
            '----------|---------|\n'
            'line1     | x     |\\\n'
            'line2     | y     |\\\n'
            'line3     | z     |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th><th>B</th></tr></thead>'
            '<tbody><tr>'
            '<td><p>line1 line2 line3</p></td>'
            '<td><p>x y z</p></td>'
            '</tr></tbody></table>',
            multiline=True,
        )

    def test_multiline_colspan_preserved(self):
        src = (
            'A      | B     | C     | D     | E\n'
            '-------|-------|-------|-------|------\n'
            'large  || another      |||\\\n'
            'cont   || cont2        |||\\\n'
            'end    || end2         |||'
        )
        assert_html(
            src,
            '<table><thead><tr>'
            '<th>A</th><th>B</th><th>C</th><th>D</th><th>E</th>'
            '</tr></thead><tbody><tr>'
            '<td colspan="2"><p>large cont end</p></td>'
            '<td colspan="3"><p>another cont2 end2</p></td>'
            '</tr></tbody></table>',
            multiline=True,
        )

    def test_multiline_disabled_backslash_is_literal(self):
        '''With multiline=False (default), backslash is kept as cell content.'''
        src = (
            'A | B\n'
            '--|--\n'
            '1 | 2 \\'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th><th>B</th></tr></thead>'
            '<tbody><tr><td>1</td><td>2 \\</td></tr></tbody></table>',
        )

    def test_multiline_backslash_only_at_end_of_header_row(self):
        '''A backslash at the end of the header row itself has no effect.'''
        src = (
            'A         | B     |\\\n'
            '----------|---------|\n'
            'text:     | 1     |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th><th>B</th></tr></thead>'
            '<tbody><tr><td>text:</td><td>1</td></tr></tbody></table>',
            multiline=True,
        )
