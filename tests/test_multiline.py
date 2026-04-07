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

    def test_multiline_codeblocks(self):
        '''Backslash continuation works within fenced code blocks.'''
        src = (
            '| A | B |\n'
            '|--|--|\n'
            '| ```   | - item 1 | \\\n'
            '| line1 | - item 2 | \\\n'
            '| line2 |          | \\\n'
            '| ```   |          |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th><th>B</th></tr></thead>'
            '<tbody><tr><td>'
            '<pre><code>line1\nline2\n</code></pre>'
            '</td><td>'
            '<ul><li>item 1</li><li>item 2</li></ul>'
            '</td></tr></tbody></table>',
            extensions=['pymdown_multimd_table', 'fenced_code'],
            multiline=True,
        )

    def test_multiline_fenced_code_with_language(self):
        '''Fenced code blocks with a language annotation work inside multiline cells.'''
        src = (
            '| A |\n'
            '|--|\n'
            '| ```python | \\\n'
            '| x = 1     | \\\n'
            '| ```       |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th></tr></thead>'
            '<tbody><tr><td>'
            '<pre><code class="language-python">x = 1\n</code></pre>'
            '</td></tr></tbody></table>',
            extensions=['pymdown_multimd_table', 'fenced_code'],
            multiline=True,
        )

    def test_multiline_blockquote(self):
        '''Block quotes work inside multiline cells.'''
        src = (
            '| A               | B     |\n'
            '|--|--|\n'
            '| > quote line 1  | other | \\\n'
            '| > quote line 2  |       |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th><th>B</th></tr></thead>'
            '<tbody><tr>'
            '<td><blockquote><p>quote line 1\nquote line 2</p></blockquote></td>'
            '<td><p>other</p></td>'
            '</tr></tbody></table>',
            multiline=True,
        )

    def test_multiline_nested_list(self):
        '''Relative indentation is preserved so nested lists work inside multiline cells.'''
        src = (
            '| A |\n'
            '|--|\n'
            '| - item 1       | \\\n'
            '|     - sub 1    | \\\n'
            '|     - sub 2    | \\\n'
            '| - item 2       |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th></tr></thead>'
            '<tbody><tr><td>'
            '<ul>'
            '<li>item 1<ul><li>sub 1</li><li>sub 2</li></ul></li>'
            '<li>item 2</li>'
            '</ul>'
            '</td></tr></tbody></table>',
            multiline=True,
        )

    def test_multiline_admonition(self):
        '''Admonition blocks work inside multiline cells (requires admonition extension).'''
        src = (
            '| A |\n'
            '|--|\n'
            '| !!! note      | \\\n'
            '|     Hello     |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th></tr></thead>'
            '<tbody><tr><td>'
            '<div class="admonition note">'
            '<p class="admonition-title">Note</p>'
            '<p>Hello</p>'
            '</div>'
            '</td></tr></tbody></table>',
            extensions=['pymdown_multimd_table', 'admonition'],
            multiline=True,
        )

    def test_multiline_admonition_with_title(self):
        '''Admonitions with a custom title work inside multiline cells.'''
        src = (
            '| A |\n'
            '|--|\n'
            '| !!! info "My Title" | \\\n'
            '|     Content here    |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th></tr></thead>'
            '<tbody><tr><td>'
            '<div class="admonition info">'
            '<p class="admonition-title">My Title</p>'
            '<p>Content here</p>'
            '</div>'
            '</td></tr></tbody></table>',
            extensions=['pymdown_multimd_table', 'admonition'],
            multiline=True,
        )

    def test_multiline_definition_list(self):
        '''Definition lists work inside multiline cells (requires def_list extension).'''
        src = (
            '| A |\n'
            '|--|\n'
            '| Apple        | \\\n'
            '| :   A fruit  |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th></tr></thead>'
            '<tbody><tr><td>'
            '<dl><dt>Apple</dt><dd>A fruit</dd></dl>'
            '</td></tr></tbody></table>',
            extensions=['pymdown_multimd_table', 'def_list'],
            multiline=True,
        )
