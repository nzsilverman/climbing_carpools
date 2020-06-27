class WSCell:
    """
    A spreadsheet cell defined by a row and column
    """

    def __init__(self, row, col):

        self.row = row
        self.col = col

    def __get_column(self, id):
        """
        Converts an integer column into a spreadsheet column

        1 -> A
        2 -> B
        27 -> AA
        """

        column_name = ""

        while id > 0:
            id, remainder = divmod(id - 1, 26)
            column_name = chr(65 + remainder) + column_name

        return column_name

    def getA1(self):
        """
        Returns cell posiiton in A1 notation
        """

        return self.__get_column(self.col) + str(self.row)

    def get(self):
        """
        Get integer cell coordinates
        """

        return self.row, self.col

    def inc_row(self, increment):
        """
        Increment row index by increment amount
        """

        self.row += increment

    def inc_col(self, increment):
        """
        Increment column index by increment amount
        """

        self.col += increment
