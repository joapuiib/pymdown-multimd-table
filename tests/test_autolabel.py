'''Tests for auto-generated caption IDs (autolabel option).'''

from __future__ import annotations

from tests.conftest import assert_html


class TestAutolabel:
    def test_autolabel_enabled_generates_id(self):
        '''With autolabel=True (default), caption text becomes the id.'''
        src = (
            '[My Table]\n'
            '| A |\n'
            '| - |\n'
            '| 1 |'
        )
        assert_html(
            src,
            '<table><caption id="mytable">My Table</caption>'
            '<thead><tr><th>A</th></tr></thead>'
            '<tbody><tr><td>1</td></tr></tbody></table>',
            autolabel=True,
        )

    def test_autolabel_disabled_no_id_generated(self):
        '''With autolabel=False, unlabelled captions have no id attribute.'''
        src = (
            '| - |\n'
            '| 1 |\n'
            '[nolabel]'
        )
        assert_html(
            src,
            '<table><caption style="caption-side: bottom">nolabel</caption>'
            '<tbody><tr><td>1</td></tr></tbody></table>',
            headerless=True,
            autolabel=False,
        )

    def test_autolabel_disabled_explicit_label_still_works(self):
        '''With autolabel=False, an explicit [text][label] still sets the id.'''
        src = (
            '[My Table][explicit]\n'
            '| A |\n'
            '| - |\n'
            '| 1 |'
        )
        assert_html(
            src,
            '<table><caption id="explicit">My Table</caption>'
            '<thead><tr><th>A</th></tr></thead>'
            '<tbody><tr><td>1</td></tr></tbody></table>',
            autolabel=False,
        )

    def test_autolabel_label_normalization(self):
        '''Label is lowercased and non-word characters are removed.'''
        src = (
            '[Hello, World! 2024]\n'
            '| A |\n'
            '| - |\n'
            '| 1 |'
        )
        assert_html(
            src,
            '<table><caption id="helloworld2024">Hello, World! 2024</caption>'
            '<thead><tr><th>A</th></tr></thead>'
            '<tbody><tr><td>1</td></tr></tbody></table>',
            autolabel=True,
        )
