from unittest import TestCase
from nose2.tools import params

from scheduler.classes.WSCell import WSCell
from scheduler.classes.WSRange import WSRange


class WSRangeTest(TestCase):

    ws_range_basic = [
        (4, 4, 4, 6, "D4:F4"),
        (1, 1, 1, 1, "A1:A1"),
        (5, 6, 7, 7, "E6:G7"),
    ]

    @params(ws_range_basic[0], ws_range_basic[1])
    def test_ws_range_basic(self, row1, col1, row2, col2, check):
        start = WSCell(row1, col1)
        end = WSCell(row2, col2)

        r = WSRange(start, end)

        self.assertEqual(r.getA1(), check)


class WSCellTest(TestCase):

    ws_basic_test = [(2, 3, 2, 3), (1, 2, 1, 2)]

    column_increment_test_data = [(4, 5, 5, 10), (1, 2, -1, 1)]

    row_increment_test_data = [(4, 5, 5, 9), (1, 2, -1, 0)]

    get_a1_test_data = [(4,)]

    @params(ws_basic_test[0], ws_basic_test[1])
    def test_ws_cell_basic(self, row, column, check_row, check_column):
        r = WSCell(row, column)
        self.assertEqual(r.get()[0], check_row)
        self.assertEqual(r.get()[1], check_column)

    @params(column_increment_test_data[0], column_increment_test_data[1])
    def test_column_increment(self, row, column, increment, check):
        r = WSCell(row, column)
        r.inc_col(increment)
        self.assertEqual(r.get()[1], check)

    @params(row_increment_test_data[0], row_increment_test_data[1])
    def test_column_increment(self, row, column, increment, check):
        r = WSCell(row, column)
        r.inc_row(increment)
        self.assertEqual(r.get()[0], check)
