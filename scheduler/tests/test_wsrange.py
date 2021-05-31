from unittest import TestCase

from nose2.tools import params

from scheduler.classes.WSCell import WSCell
from scheduler.classes.WSRange import WSRange
from test_data import WSRangeTestData, WSCellTestData


class WSRangeTest(TestCase):
    """
    Tests WSRange
    """

    ws_range_basic = WSRangeTestData.ws_range_basic

    @params(ws_range_basic[0], ws_range_basic[1])
    def test_ws_range_basic(self, row1, col1, row2, col2, check):
        start = WSCell(row1, col1)
        end = WSCell(row2, col2)

        r = WSRange(start, end)

        self.assertEqual(r.getA1(), check)


class WSCellTest(TestCase):
    """
    Tests WSCell
    """

    ws_basic_test = WSCellTestData.ws_basic_test
    column_increment_test_data = WSCellTestData.column_increment_test_data
    row_increment_test_data = WSCellTestData.row_increment_test_data
    get_a1_test_data = WSCellTestData.get_a1_test_data

    @params(ws_basic_test[0], ws_basic_test[1])
    def test_ws_cell_basic(self, row, column, check_row, check_column):
        cell = WSCell(row, column)
        self.assertEqual(cell.get()[0], check_row)
        self.assertEqual(cell.get()[1], check_column)

    @params(column_increment_test_data[0], column_increment_test_data[1])
    def test_column_increment(self, row, column, increment, check):
        cell = WSCell(row, column)
        cell.inc_col(increment)
        self.assertEqual(cell.get()[1], check)

    @params(row_increment_test_data[0], row_increment_test_data[1])
    def test_column_increment(self, row, column, increment, check):
        cell = WSCell(row, column)
        cell.inc_row(increment)
        self.assertEqual(cell.get()[0], check)

    @params(get_a1_test_data[0])
    def test_get_a1(self, row, col, check):
        cell = WSCell(row, col)
        r = cell.getA1()
        self.assertEqual(r, check)
