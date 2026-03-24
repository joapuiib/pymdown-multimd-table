'''Tests for multiple header rows.'''

from __future__ import annotations

from tests.conftest import assert_html


class TestMultipleHeaders:
    def test_two_header_rows(self):
        src = (
            '| Group1 | Group2 |\n'
            '| A      | B      |\n'
            '| ------ | ------ |\n'
            '| 1      | 2      |'
        )
        assert_html(
            src,
            '<table><thead>'
            '<tr><th>Group1</th><th>Group2</th></tr>'
            '<tr><th>A</th><th>B</th></tr>'
            '</thead><tbody>'
            '<tr><td>1</td><td>2</td></tr>'
            '</tbody></table>',
        )

    def test_three_header_rows(self):
        src = (
            '| L1A | L1B |\n'
            '| L2A | L2B |\n'
            '| L3A | L3B |\n'
            '| --- | --- |\n'
            '| d   | e   |'
        )
        assert_html(
            src,
            '<table><thead>'
            '<tr><th>L1A</th><th>L1B</th></tr>'
            '<tr><th>L2A</th><th>L2B</th></tr>'
            '<tr><th>L3A</th><th>L3B</th></tr>'
            '</thead><tbody>'
            '<tr><td>d</td><td>e</td></tr>'
            '</tbody></table>',
        )
