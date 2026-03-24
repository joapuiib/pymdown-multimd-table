'''Tests for headerless tables (headerless option).'''

from __future__ import annotations

from tests.conftest import convert, assert_html


class TestHeaderless:
    '''headerless=True allows tables without a header/separator row.'''

    def test_simplest_headerless(self):
        src = (
            '|---|---|\n'
            '|data|row|'
        )
        assert_html(
            src,
            '<table><tbody><tr><td>data</td><td>row</td></tr></tbody></table>',
            headerless=True,
        )

    def test_headerless_with_alignment(self):
        src = (
            '| :- | -: |\n'
            '| L  | R  |'
        )
        assert_html(
            src,
            '<table><tbody><tr>'
            '<td style="text-align:left">L</td>'
            '<td style="text-align:right">R</td>'
            '</tr></tbody></table>',
            headerless=True,
        )

    def test_headerless_multiple_rows(self):
        src = (
            '|---|---|\n'
            '| a | b |\n'
            '| c | d |'
        )
        assert_html(
            src,
            '<table><tbody>'
            '<tr><td>a</td><td>b</td></tr>'
            '<tr><td>c</td><td>d</td></tr>'
            '</tbody></table>',
            headerless=True,
        )

    def test_separator_only_is_not_a_headerless_table(self):
        '''A separator with no data rows should not produce a table.'''
        src = '|---|---|---|'
        result = convert(src, headerless=True)
        assert '<table>' not in result

    def test_separator_with_empty_row_is_not_a_table(self):
        '''A separator followed by a row with no valid pipes is not a table.'''
        src = (
            '|---|---|---|\n'
            '|'
        )
        result = convert(src, headerless=True)
        assert '<table>' not in result

    def test_headerless_disabled_separator_required(self):
        '''With headerless=False (default), a separator row is mandatory.'''
        src = (
            '|---|---|\n'
            '| a | b |'
        )
        result = convert(src)  # headerless=False by default
        # Without a proper header row before separator, treated as a table
        # starting with a headerless body — but default mode requires header.
        # The separator-only is invalid → not a table.
        assert '<table>' not in result
