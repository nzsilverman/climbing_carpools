from scheduler.classes.WSCell import WSCell
from scheduler.classes.Configuration import Configuration


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


class CarBlock:
    """Spreadsheet ranges corresponding to a car's output block

        Attributes:
            upper_left:
            upper_right:
            lower_right:
            lower_left:
            block_length:
    """

    def __init__(self, start_row: int, end_row: int, start_col: int,
                 end_col: int):
        """Initializer for CarBlock

        Initialize a car block using the first car to set the relative size.

            Args:
                start_row:
                    The starting row index
                end_row:
                    The ending row index
                start_col:
                    The starting column index
                end_col:
                    The ending column index

        Typical Usage:

            block = CarBlock(0, 0, 5, 5)

            for car in day:
                block.update_block_length(car.seats)
                .
                .
                # use getters to select ranges in the car block
                .
                .
                block.move_to_next()

        """
        self.upper_left = WSCell(start_row, start_col)
        self.upper_right = WSCell(start_row, end_col)
        self.lower_right = WSCell(end_row, end_col)
        self.lower_left = WSCell(end_row, start_col)
        self.block_length = 0
        self.block_spacing = Configuration.config(
            "gform_backend.output.car_block_spacing")

    def update_block_length(self, seats: int):
        """Updates the block length for next car.

            Args:
                seats:
                    Number of seats in the current car
        """
        # + 1 for heading
        # + 1 for driver row
        self.block_length = seats + 2

        # move lower left and right down to set the lower bounds of the range
        self.lower_right.inc_row(self.block_length)
        self.lower_left.inc_row(self.block_length)

    def get_car_block_a1_range(self) -> str:
        """Get the A1 range of the entire car block

            Returns:
                An A1 range string for the car block

        """
        return WSRange(self.upper_left, self.lower_right).getA1()

    def get_car_heading_a1_range(self) -> str:
        """Get the A1 range of the car block's heading

            Returns:
                An A1 range string for the car block's heading

        """

        return WSRange(self.upper_left, self.upper_right).getA1()

    def get_car_roles_a1_range(self) -> str:
        """Get the A1 range of the member roles in a car block

            Returns:
                An A1 range string for the member roles in a car block

        """
        return WSRange(self.upper_left, self.lower_left).getA1()

    def move_to_next(self):
        """Moves block down to next location.
        """
        # these must be moved by the block length, they aren't updated when setting the
        # initial car block size
        self.upper_left.inc_row(self.block_spacing + self.block_length)
        self.upper_right.inc_row(self.block_spacing + self.block_length)

        # updated by block_length when updating block_length for new car
        self.lower_right.inc_row(self.block_spacing)
        self.lower_left.inc_row(self.block_spacing)
