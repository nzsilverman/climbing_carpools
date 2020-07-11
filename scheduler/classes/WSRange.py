from scheduler.classes.WSCell import WSCell


# TODO -> Why does this need to be a class?
class WSRange:
    """A spreadsheet range defined by a starting and ending cells.
    """

    def __init__(self, start: WSCell, end: WSCell):
        """
        Creates a range from a starting cell and ending cell
        """

        self.start = start
        self.end = end

    def getA1(self) -> str:
        """
        Returns a spreadsheet range in A1 notation

        A1:A1
        """

        return self.start.getA1() + ":" + self.end.getA1()
