# TODO-> why does this need to be a class versus a helper file?
class WSCell:
    """A spreadsheet cell defined by a row and column.

        Attributes:
            row:
                spreadsheet row
            col:
                spreadsheet column
    """

    def __init__(self, row: int, col: int):

        self.row = row
        self.col = col

    def _get_column(self, id: int) -> str:
        """Converts an integer column into a spreadsheet column.

        1 -> A
        2 -> B
        27 -> AA
        """

        column_name = ""

        while id > 0:
            id, remainder = divmod(id - 1, 26)
            column_name = chr(65 + remainder) + column_name

        return column_name

    def getA1(self) -> str:
        """Returns cell posiiton in A1 notation
        """

        return self._get_column(self.col) + str(self.row)

    def get_column(self) -> str:
        """
        Returns column as letter
        """
        return self._get_column(self.col)

    def get(self) -> (int, int):
        """
        Get integer cell coordinates
        """

        return self.row, self.col

    def inc_row(self, increment: int) -> None:
        """
        Increment row index by increment amount
        """

        self.row += increment

    def inc_col(self, increment: int) -> None:
        """
        Increment column index by increment amount
        """

        self.col += increment
