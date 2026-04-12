'''Tests for attribute list syntax on cells and rows (attr_list option).'''

from __future__ import annotations

from tests.conftest import assert_html, convert


class TestAttrList:
    '''attr_list=True enables {.class #id key=val} on cells and rows.'''

    # ------------------------------------------------------------------
    # Cell-level attributes
    # ------------------------------------------------------------------

    def test_cell_class(self):
        '''A trailing {.class} in a cell is stripped and applied to the element.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| cell {.myclass} |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr><td class="myclass">cell</td></tr></tbody></table>',
            attr_list=True,
        )

    def test_cell_id(self):
        '''A trailing {#id} in a cell sets the id attribute.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| cell {#myid} |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr><td id="myid">cell</td></tr></tbody></table>',
            attr_list=True,
        )

    def test_cell_key_value(self):
        '''A trailing {key="value"} in a cell sets an arbitrary attribute.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| cell {data-foo="bar"} |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr><td data-foo="bar">cell</td></tr></tbody></table>',
            attr_list=True,
        )

    def test_cell_multiple_classes(self):
        '''Multiple .class tokens accumulate on the class attribute.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| cell {.c1 .c2} |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr><td class="c1 c2">cell</td></tr></tbody></table>',
            attr_list=True,
        )

    def test_header_cell_attrs(self):
        '''Attrs can be applied to <th> cells.'''
        src = (
            '| H {.hdr} |\n'
            '| - |\n'
            '| cell |'
        )
        assert_html(
            src,
            '<table><thead><tr><th class="hdr">H</th></tr></thead>'
            '<tbody><tr><td>cell</td></tr></tbody></table>',
            attr_list=True,
        )

    def test_cell_attrs_on_one_of_many_cells(self):
        '''Only the cell that carries {…} receives the attribute.'''
        src = (
            '| A | B |\n'
            '| - | - |\n'
            '| x {.myclass} | y |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th><th>B</th></tr></thead>'
            '<tbody><tr><td class="myclass">x</td><td>y</td></tr></tbody></table>',
            attr_list=True,
        )

    def test_cell_class_combined_with_wrap(self):
        """Custom class appends to the wrappable 'extend' class."""
        src = (
            '| H |\n'
            '| -+ |\n'
            '| cell {.myclass} |'
        )
        assert_html(
            src,
            '<table><thead><tr><th class="extend">H</th></tr></thead>'
            '<tbody><tr><td class="extend myclass">cell</td></tr></tbody></table>',
            attr_list=True,
        )

    def test_cell_class_combined_with_alignment(self):
        '''Custom class and alignment style coexist on the same element.'''
        src = (
            '| H |\n'
            '| -: |\n'
            '| cell {.myclass} |'
        )
        assert_html(
            src,
            '<table><thead><tr><th style="text-align:right">H</th></tr></thead>'
            '<tbody><tr><td class="myclass" style="text-align:right">cell</td></tr></tbody></table>',
            attr_list=True,
        )

    def test_cell_attrs_with_rowspan(self):
        '''Cell attrs are preserved when the cell also has a rowspan.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| A {.cls} |\n'
            '| ^^ |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr><td class="cls" rowspan="2">A</td></tr><tr></tr></tbody></table>',
            rowspan=True,
            attr_list=True,
        )

    # ------------------------------------------------------------------
    # Cell-level edge cases
    # ------------------------------------------------------------------

    def test_cell_id_and_class_combined(self):
        '''Both #id and .class can appear together in a single cell {…} block.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| cell {#myid .myclass} |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr><td class="myclass" id="myid">cell</td></tr></tbody></table>',
            attr_list=True,
        )

    def test_cell_all_attr_types_combined(self):
        '''id, class, and key=value can all be specified in a single cell {…} block.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| cell {#myid .myclass data-x="1"} |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr><td class="myclass" data-x="1" id="myid">cell</td></tr></tbody></table>',
            attr_list=True,
        )

    def test_cell_attrs_on_colspan_cell(self):
        '''Attrs on a cell that also has a colspan are preserved.'''
        src = (
            '| A | B | C |\n'
            '| - | - | - |\n'
            '| wide {.wide} || x |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th><th>B</th><th>C</th></tr></thead>'
            '<tbody><tr><td class="wide" colspan="2">wide</td><td>x</td></tr></tbody></table>',
            attr_list=True,
        )

    def test_cell_attrs_on_multiple_cells_in_same_row(self):
        '''Each cell can independently carry its own {…} attributes.'''
        src = (
            '| A | B |\n'
            '| - | - |\n'
            '| x {.cls1} | y {.cls2} |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th><th>B</th></tr></thead>'
            '<tbody><tr><td class="cls1">x</td><td class="cls2">y</td></tr></tbody></table>',
            attr_list=True,
        )

    # ------------------------------------------------------------------
    # Row-level attributes
    # ------------------------------------------------------------------

    def test_row_class(self):
        '''A trailing {.class} after the last pipe is applied to <tr>.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| cell |{.myrow}'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr class="myrow"><td>cell</td></tr></tbody></table>',
            attr_list=True,
        )

    def test_row_id(self):
        '''A trailing {#id} after the last pipe sets the id on <tr>.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| cell | {#myrow}'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr id="myrow"><td>cell</td></tr></tbody></table>',
            attr_list=True,
        )

    def test_row_attrs_on_multi_column_row(self):
        '''Row attrs work when the row has multiple cells.'''
        src = (
            '| A | B |\n'
            '| - | - |\n'
            '| x | y |{.myrow}'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th><th>B</th></tr></thead>'
            '<tbody><tr class="myrow"><td>x</td><td>y</td></tr></tbody></table>',
            attr_list=True,
        )

    def test_row_attrs_on_header_row(self):
        '''Row attrs can be applied to header rows.'''
        src = (
            '| H {.hdr} |{.hdrrow}\n'
            '| - |\n'
            '| cell |'
        )
        assert_html(
            src,
            '<table><thead><tr class="hdrrow"><th class="hdr">H</th></tr></thead>'
            '<tbody><tr><td>cell</td></tr></tbody></table>',
            attr_list=True,
        )

    def test_row_key_value(self):
        '''A key=value attribute after the last pipe is set on <tr>.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| cell |{data-section="main"}'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr data-section="main"><td>cell</td></tr></tbody></table>',
            attr_list=True,
        )

    def test_row_id_and_class_combined(self):
        '''Both #id and .class can be set on a row in a single {…} block.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| cell |{#myid .myrow}'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr class="myrow" id="myid"><td>cell</td></tr></tbody></table>',
            attr_list=True,
        )

    def test_multiple_rows_each_with_own_attrs(self):
        '''Every row can independently carry its own row-level {…} attributes.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| a |{.row-a}\n'
            '| b |{.row-b}\n'
            '| c |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody>'
            '<tr class="row-a"><td>a</td></tr>'
            '<tr class="row-b"><td>b</td></tr>'
            '<tr><td>c</td></tr>'
            '</tbody></table>',
            attr_list=True,
        )

    # ------------------------------------------------------------------
    # Cell + row combined
    # ------------------------------------------------------------------

    def test_cell_and_row_attrs_combined(self):
        '''Cell and row attrs can be used together on the same row.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| cell {.myclass} |{.myrow}'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr class="myrow"><td class="myclass">cell</td></tr></tbody></table>',
            attr_list=True,
        )

    # ------------------------------------------------------------------
    # Multiline cells
    # ------------------------------------------------------------------

    def test_multiline_cell_attrs_on_last_segment(self):
        '''Cell attrs on the last continuation line are applied to the <td>.'''
        src = (
            'A    | B\n'
            '-----|-----\n'
            'line1| x  \\\n'
            'line2| y {.mycell}'
        )
        assert_html(
            src,
            '<table><thead><tr><th>A</th><th>B</th></tr></thead>'
            '<tbody><tr><td><p>line1 line2</p></td>'
            '<td class="mycell"><p>x y</p></td></tr></tbody></table>',
            multiline=True,
            attr_list=True,
        )

    # ------------------------------------------------------------------
    # Disabled (default behaviour)
    # ------------------------------------------------------------------

    def test_attr_list_disabled_curly_braces_are_literal(self):
        '''{…} is rendered as literal cell content when attr_list=False.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| cell {.myclass} |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr><td>cell {.myclass}</td></tr></tbody></table>',
        )

    def test_attr_list_disabled_row_braces_become_extra_cell(self):
        '''{…} after the last pipe becomes an extra cell when attr_list=False.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| cell |{.myrow}'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr><td>cell</td><td>{.myrow}</td></tr></tbody></table>',
        )

    # ------------------------------------------------------------------
    # Integration with the attr_list Markdown extension
    # ------------------------------------------------------------------

    def test_compatible_with_attr_list_extension(self):
        '''Our attr_list option and the attr_list extension produce the same result.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| cell {.myclass} |{.myrow}'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr class="myrow"><td class="myclass">cell</td></tr></tbody></table>',
            extensions=['pymdown_multimd_table', 'attr_list'],
            attr_list=True,
        )

    # ------------------------------------------------------------------
    # Table-level attributes
    # ------------------------------------------------------------------

    def test_table_attrs_class(self):
        '''A standalone {…} on the last line is applied to the <table> element.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| cell |\n'
            '{.mytable}'
        )
        assert_html(
            src,
            '<table class="mytable"><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr><td>cell</td></tr></tbody></table>',
            attr_list=True,
        )

    def test_table_attrs_id(self):
        '''A standalone {#id} on the last line sets id on the <table>.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| cell |\n'
            '{#mytable}'
        )
        assert_html(
            src,
            '<table id="mytable"><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr><td>cell</td></tr></tbody></table>',
            attr_list=True,
        )

    def test_table_attrs_multiple(self):
        '''Multiple attributes on the table.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| cell |\n'
            '{#mytable .myclass data-x=y}'
        )
        assert_html(
            src,
            '<table class="myclass" data-x="y" id="mytable"><thead><tr><th>H</th></tr></thead>'
            '<tbody><tr><td>cell</td></tr></tbody></table>',
            attr_list=True,
        )

    def test_table_attrs_ignored_when_disabled(self):
        '''Standalone {…} on the last line is NOT consumed as attrs when attr_list=False.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| cell |\n'
            '{.mytable}'
        )
        # With attr_list disabled the line is not part of the table block; the
        # table ends before it, so it should be rendered as a paragraph.
        result = convert(src)
        assert '<table class="mytable">' not in result

    # ------------------------------------------------------------------
    # Tbody-level attributes
    # ------------------------------------------------------------------

    def test_tbody_attrs_class(self):
        '''A standalone {…} line after a tbody closes the tbody and applies attrs to it.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| row1 |\n'
            '{.mybody}\n'
            '\n'
            '| row2 |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody class="mybody"><tr><td>row1</td></tr></tbody>'
            '<tbody><tr><td>row2</td></tr></tbody></table>',
            attr_list=True,
            multibody=True,
        )

    def test_tbody_attrs_id(self):
        '''A standalone {#id} applies an id to the preceding tbody.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| row1 |\n'
            '{#first}\n'
            '\n'
            '| row2 |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody id="first"><tr><td>row1</td></tr></tbody>'
            '<tbody><tr><td>row2</td></tr></tbody></table>',
            attr_list=True,
            multibody=True,
        )

    def test_tbody_attrs_multiple(self):
        '''Multiple attributes on a tbody.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| row1 |\n'
            '{#first .mybody data-x=y}\n'
            '\n'
            '| row2 |'
        )
        assert_html(
            src,
            '<table><thead><tr><th>H</th></tr></thead>'
            '<tbody class="mybody" data-x="y" id="first"><tr><td>row1</td></tr></tbody>'
            '<tbody><tr><td>row2</td></tr></tbody></table>',
            attr_list=True,
            multibody=True,
        )

    def test_tbody_attrs_all_bodies(self):
        '''The last {…} becomes a table attr; earlier {…} before blank lines are tbody attrs.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| row1 |\n'
            '{.first}\n'
            '\n'
            '| row2 |\n'
            '{.second}'
        )
        # {.first} is before a blank line → tbody attr for the first tbody.
        # {.second} is the very last line (no blank line after) → table attr.
        assert_html(
            src,
            '<table class="second"><thead><tr><th>H</th></tr></thead>'
            '<tbody class="first"><tr><td>row1</td></tr></tbody>'
            '<tbody><tr><td>row2</td></tr></tbody></table>',
            attr_list=True,
            multibody=True,
        )

    def test_tbody_attrs_ignored_when_disabled(self):
        '''Standalone {…} before blank line is treated as a new tbody separator row (invalid) when attr_list=False, so the block is not consumed.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| row1 |\n'
            '{.mybody}\n'
            '\n'
            '| row2 |'
        )
        # Without attr_list the {…} line breaks multibody detection; the table
        # ends at row1 and the remaining lines become separate blocks.
        result = convert(src, multibody=True)
        assert '<tbody class="mybody">' not in result

    def test_tbody_and_table_attrs_combined(self):
        '''Two consecutive {…} at the end: first = tbody attr, second = table attr.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| row |\n'
            '{.last-tbody}\n'
            '{.whole-table}'
        )
        assert_html(
            src,
            '<table class="whole-table"><thead><tr><th>H</th></tr></thead>'
            '<tbody class="last-tbody"><tr><td>row</td></tr></tbody></table>',
            attr_list=True,
            multibody=True,
        )

    def test_tbody_and_table_attrs_combined_multibody(self):
        '''First tbody attr (before blank), second tbody attr + table attr at end.'''
        src = (
            '| H |\n'
            '| - |\n'
            '| row1 |\n'
            '{.first}\n'
            '\n'
            '| row2 |\n'
            '{.second}\n'
            '{.mytable}'
        )
        assert_html(
            src,
            '<table class="mytable"><thead><tr><th>H</th></tr></thead>'
            '<tbody class="first"><tr><td>row1</td></tr></tbody>'
            '<tbody class="second"><tr><td>row2</td></tr></tbody></table>',
            attr_list=True,
            multibody=True,
        )
