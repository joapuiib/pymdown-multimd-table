'''Tests for table captions ([text] and [text][label] syntax).'''

from __future__ import annotations

from tests.conftest import assert_html


class TestCaptions:
    def test_caption_before_table(self):
        src = (
            '[My Caption]\n'
            '| A |\n'
            '| - |\n'
            '| 1 |'
        )
        assert_html(
            src,
            '<table><caption id="mycaption">My Caption</caption>'
            '<thead><tr><th>A</th></tr></thead>'
            '<tbody><tr><td>1</td></tr></tbody></table>',
        )

    def test_caption_after_table(self):
        src = (
            '| A |\n'
            '| - |\n'
            '| 1 |\n'
            '[My Caption]'
        )
        assert_html(
            src,
            '<table><caption id="mycaption" style="caption-side: bottom">My Caption</caption>'
            '<thead><tr><th>A</th></tr></thead>'
            '<tbody><tr><td>1</td></tr></tbody></table>',
        )

    def test_caption_autolabel_generates_id(self):
        src = (
            '[Prototype Table]\n'
            '| A |\n'
            '| - |\n'
            '| 1 |'
        )
        assert_html(
            src,
            '<table><caption id="prototypetable">Prototype Table</caption>'
            '<thead><tr><th>A</th></tr></thead>'
            '<tbody><tr><td>1</td></tr></tbody></table>',
        )

    def test_caption_explicit_label(self):
        src = (
            '[My Table][tbl1]\n'
            '| A |\n'
            '| - |\n'
            '| 1 |'
        )
        assert_html(
            src,
            '<table><caption id="tbl1">My Table</caption>'
            '<thead><tr><th>A</th></tr></thead>'
            '<tbody><tr><td>1</td></tr></tbody></table>',
        )

    def test_caption_explicit_label_overrides_autolabel(self):
        src = (
            '[Long Name][short]\n'
            '| A |\n'
            '| - |\n'
            '| 1 |'
        )
        assert_html(
            src,
            '<table><caption id="short">Long Name</caption>'
            '<thead><tr><th>A</th></tr></thead>'
            '<tbody><tr><td>1</td></tr></tbody></table>',
        )

    def test_only_first_caption_used(self):
        '''When both before and after captions are in one block, only the first wins.
        The second caption is consumed by the DFA (state → 0x00000) but discarded.
        '''
        src = (
            '[First]\n'
            '| A |\n'
            '| - |\n'
            '| 1 |\n'
            '[Second]'
        )
        assert_html(
            src,
            '<table><caption id="first">First</caption>'
            '<thead><tr><th>A</th></tr></thead>'
            '<tbody><tr><td>1</td></tr></tbody></table>',
        )

    def test_caption_label_lowercased_and_stripped(self):
        '''Label derived from caption text: lowercased, non-word chars removed.'''
        src = (
            '[Hello, World! 42]\n'
            '| A |\n'
            '| - |\n'
            '| 1 |'
        )
        assert_html(
            src,
            '<table><caption id="helloworld42">Hello, World! 42</caption>'
            '<thead><tr><th>A</th></tr></thead>'
            '<tbody><tr><td>1</td></tr></tbody></table>',
        )

    def test_not_a_caption_inside_table(self):
        '''[...] on a line that is already inside the table rows is not a caption.'''
        src = (
            '| A |\n'
            '| - |\n'
            '| [not a caption] |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th></tr></thead><tbody>'
            '<tr><td>[not a caption]</td></tr>'
            '</tbody></table>',
        )
