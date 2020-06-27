class WSCell:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __get_column(self, id):
        column_name = ""

        while id > 0:
            id, remainder = divmod(id - 1, 26)
            column_name = chr(65 + remainder) + column_name
        
        return column_name

    def getA1(self):
        return self.__get_column(self.col) + str(self.row) 

    def get(self):
        return self.row, self.col
    
    def inc_row(self, increment):
        self.row += increment

    def inc_col(self, increment):
        self.col += increment