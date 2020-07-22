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
    """Spreadsheet ranges corresponding to a car's output block.
    A single CarBlock object is created and then moved moved to
    the next car location every loop.

    The block_length must be set before using any of the ranges
    provided by the CarBlock.

        Attributes:
            upper_left:
                WSCell object representing the upper left cell of a car block
            upper_right:
                WSCell object representing the upper right cell of a car block
            lower_right:
                WSCell object representing the lower right cell of a car block
                Initially not set until block_length is updated for the current
                car
            lower_left:
                WSCell object representing the lower left cell of a car block
                Initially not set until block_length is updated for the current
                car
            block_length:
                The length of the car block, changes car-to-car based on
                the number seats in the car. Since this changes car-to-car
                and is used to compute the A1 ranges, it needs to be set in the
                beginning of every loop. We don't know the number of seats in a 
                car until we start iterating so it must be set in the beginning
                of each loop.

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
