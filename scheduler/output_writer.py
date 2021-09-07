"""Backend for reading and writing data with Google Sheets/

Reads form responses and due paying members sheet.
Writes cars with drivers and riders

Typical usage:
    import gform_backend
    <call appropriate function>

"""

import logging
from datetime import datetime
from random import uniform

import gspread
from gspread_formatting import *

import scheduler.classes.Day as Day
import scheduler.classes.MeetingLocation as MeetingLocation
from scheduler.classes.AuthorizedClient import AuthorizedClient
from scheduler.classes.Car import Car
from scheduler.classes.Configuration import Configuration
from scheduler.classes.Driver import Driver
from scheduler.classes.Member import Member
from scheduler.classes.WSCell import WSCell
from scheduler.classes.WSRange import WSRange, CarBlock

logger = logging.getLogger(__name__)


def delete_spreadsheet(name: str) -> None:
    """Deletes the spreadsheet called 'name'.
    """
    name.strip()

    client = AuthorizedClient.get_instance().client

    for s in client.openall():
        if s.title == name:
            client.del_spreadsheet(s.id)
            logger.info("Deleting spreadsheet: %s", s.title)


def create_spreadsheet() -> gspread.models.Spreadsheet:
    """Creates a spreadsheet with given name in the location defined by the folder_id.

    The folder_id can be found by viewing the folder in Drive and selecting the
    id.
    i.e:
    drive.google.com/../folders/1/<id>

    The folder id and the name of the spreadsheet to create are in the toml config files

        Returns:
            A gspread.models.Spreadsheet object
    """

    config = Configuration.config("gform_backend.files")
    client = AuthorizedClient.get_instance().client

    # checks if sheet with name already exists, deletes if exists
    if client.openall(config["output_sheet"]):
        delete_spreadsheet(config["output_sheet"])
        logger.info("Sheet exists, deleting")

    logger.info("Creating sheet")
    spreadsheet = client.create(config["output_sheet"],
                                folder_id=config["working_folder_id"])
    spreadsheet.share("rkalnins@umich.edu",
                      notify=False,
                      perm_type="user",
                      role="writer")

    return spreadsheet


def list_spreadsheets() -> None:
    """Prints spreadsheets available to the client.
    """

    client = AuthorizedClient.get_instance().client

    for s in client.openall():
        print(s.title, s.id)


def unpack_locations(member: Member, day: Day.DayName) -> str:
    """Converts locations in member's locations list to a string of location names

        Appends together all of the location strings for a particular member

        Args:
            member:
                Member object
            day:
                Day.DayName enum for which to collect locations

        Returns:
            string that is a concatenated string of all the locations a member is trying to leave from
    """

    locations = member.get_locations(day)
    location_str = ""

    for l in locations:
        location_str = location_str + MeetingLocation.to_str(l) + " "

    return location_str


def unpack_time(driver: Driver, day: Day.DayName) -> str:
    """Converts time from decimal time (hh.(mm/60)) to hh:mm <AM|PM> format

        Args:
            driver:
                Driver object
            day:
                Day.DayName enum for which to get the time

        Returns:
            Returns the unpacked time as a string, converted from (hh.(mm/60)) to (hh:mm) <AM|PM> format
    """

    time = driver.get_times(day)[0]
    dt = datetime.strptime("{0:02.0f}:{1:02.0f}".format(*divmod(time * 60, 60)),
                           "%H:%M")

    # there should only be one time for the driver
    return dt.strftime("%I:%M %p")


def get_car_block_colors() -> (float, float, float, float):
    """ Get the color parameters to use for a car box on the google sheet.

        Returns:
            (float, float, float, float)
            [0] -> r value
            [1] -> g value
            [2] -> b value
            [3] -> color alpha value
    """
    config = Configuration.config("gform_backend.output")
    colors = Configuration.config(
        "gform_backend.output.default_background_color")

    if config["random_colors"]:
        low = config["random_low_range"]
        high = config["random_high_range"]

        r = uniform(low, high)
        g = uniform(low, high)
        b = uniform(low, high)
    else:
        r = colors[0]
        g = colors[1]
        b = colors[2]

    return r, g, b, config["color_alpha"]


def format_column_widths(ws: gspread.models.Worksheet,
                         column_widths: list) -> None:
    """Sets the first n column widths for the provided worksheet where n is the
    number of provided column widths. The columns (column index > n) will be
    set using the width of column n.

        Args:
            ws:
                The worksheet for which to set the column widths
            column_widths:
                A list of column widths in pixels (int)

        Returns:
            None

    """
    widths_list = list()

    # zips a column index (1...n) to the corresponding column width defined
    # in the settings
    for (j, w) in zip(range(1, len(column_widths) + 1), column_widths):
        col_letter = WSCell(1, j).get_column()

        # we want to format the remaining columns in the sheet using
        # the width of the last sheet
        #
        # when formatting, a column with the ":" suffix represents
        # all columns to the right
        #
        # Example: The pattern "G:" matches G and all columns to the right
        # of G
        if j == len(column_widths):
            col_letter = col_letter + ":"

        widths_list.append((col_letter, w))

    set_column_widths(ws, widths_list)


def configure_sheet_title(ws: gspread.models.Worksheet,
                          day: Day.DayName) -> (str, tuple):
    """Returns the output and corresponding format for the provided sheet's title

        Args:
            ws:
                The worksheet for which to set the title
            day:
                The day which appears as a suffic to the sheet_name_base

        Returns:
            heading text:
                The text to use as the heading for the sheet
            (cell_A1A1, title_fmt):
                The range and format to use on the sheet title cell

    """
    output_config = Configuration.config("gform_backend.output")

    # title cell range
    title_range_a1 = WSRange(WSCell(
        1, 1), WSCell(1, output_config["title_cell_merge_count"])).getA1()

    cell_A1A1 = WSRange(WSCell(1, 1), WSCell(1, 1)).getA1()

    title = output_config["name"] + " — " + Day.to_str(day)

    # text for the title
    heading_text = {
        "range": cell_A1A1,
        "values": [[title]],
    }

    # format for the title
    title_fmt = cellFormat(
        textFormat=textFormat(bold=output_config["bold_title"],
                              fontSize=output_config["title_font_size"]))

    # merge the cells to make the sheet look nicer
    ws.merge_cells(title_range_a1)

    return heading_text, (cell_A1A1, title_fmt)


def get_car_output(car: Car, a1_range: str, day: Day) -> dict:
    """Returns the output for the provided car on the provided day

        Args:
            car:
                The car from which to extract content and write to the output sheet
            a1_range:
                The range of the car's output block
            day:
                The current day

        Returns:
            dict:
                dictionary of a range and values to provide to batch_update
    """

    output_config = Configuration.config("gform_backend.output")

    # add headings and driver
    car_output = {
        "range":
            a1_range,
        "values": [
            [
                "",
                "Name",
                "Car type",
                "Phone Number",
                "Departure Time",
                "Locations",
            ],
            [
                "Driver",
                car.driver.name,
                car.car_type,
                car.driver.phone,
                unpack_time(car.driver, day[0]),
                unpack_locations(car.driver, day[0]),
            ],
        ],
    }

    if output_config["notes_column"]:
        car_output["values"][0].append("Notes")
        car_output["values"][1].append("")

    # add rider info
    for r in car.riders:
        row = [
            "Rider",
            r.name,
            "",
            r.phone,
            "",
            unpack_locations(r, day[0]),
        ]

        if output_config["notes_column"]:
            row.append("")

        car_output["values"].append(row)

    return car_output


def get_starting_row_index() -> int:
    """Get the initial row index

        Returns:
            Starting row index
    """
    output_config = Configuration.config("gform_backend.output")

    # track cell indicies for sheet writing ranges
    if output_config["use_sheet_titles"]:
        # if we have a title, start 1 row down
        start_row_index = 1
    else:
        # if no title, start at row 0
        start_row_index = 0

    return start_row_index + output_config["row_buffer_top"]


def get_end_col_index(start_col_index: int) -> int:
    """Get the intial ending column index

        Args:
            start_col_index:
                The starting column index

        Returns:
            The initial ending column index
    """
    output_config = Configuration.config("gform_backend.output")

    if output_config["notes_column"]:
        # + 6 for number of columns with a notes column
        return start_col_index + 6
    else:
        # + 5 for number of columns without a notes column
        return start_col_index + 5


def get_initial_indicies() -> (int, int, int, int):
    """Get the four initial indicies:
        starting row
        starting column
        ending row
        ending column

        Returns:
            tuple
                starting row, ending row, starting column, ending column

    """
    output_config = Configuration.config("gform_backend.output")

    start_row_index = get_starting_row_index()
    end_row_index = output_config["row_buffer_top"]

    # + 1 spreadsheet columns start at index 1
    start_col_index = 1 + output_config["column_buffer_left"]
    end_col_index = get_end_col_index(start_col_index)

    return start_row_index, end_row_index, start_col_index, end_col_index


# TODO -> This function is a monster! I appreciate that it works well, but I think for maintainability it should
# be broken up into smaller functions, and needs to be more clearly labeled and commented and documented


def write_schedule(schedule: list,
                   spreadsheet: gspread.models.Spreadsheet) -> None:
    """Write schedule to provided sheet.

        Args:
            schedule:
                list of the schedule that is to be written to google sheets
            spreadsheet:
                spreadsheet to write the schedule to
    """

    # Get settings for sheet writing from configuration file
    output_config = Configuration.config("gform_backend.output")

    bold_header = output_config["bold_header"]
    bold_roles = output_config["bold_roles"]
    use_sheet_titles = output_config["use_sheet_titles"]

    general_font_size = output_config["general_font_size"]
    column_widths = output_config["column_widths"]

    # each day is a worksheet (i.e. a tab)
    for (i, day) in zip(range(0, len(schedule)), schedule):

        try:
            ws = spreadsheet.get_worksheet(i)

            ws_new = spreadsheet.duplicate_sheet(ws.id,
                                                 new_sheet_name=Day.to_str(
                                                     day[0]))
            spreadsheet.del_worksheet(ws)
            ws = ws_new
        except Exception:
            ws = spreadsheet.add_worksheet(Day.to_str(day[0]), 100, 100)

        # if the ith worksheet doesn't exist, we need to create it.
        # if it already exists, then we duplicate the existing sheet
        # and use a different name that matches the current scheme
        # and then delete the old sheet
        #
        # used when we need to delete the default sheet1
        # and create a sheet for the current day

        day_output = list()
        day_format = list()

        format_column_widths(ws, column_widths)

        # sheet titles
        if use_sheet_titles:
            outputs, formats = configure_sheet_title(ws, day[0])
            day_output.append(outputs)
            day_format.append(formats)

        start_row, end_row, start_col, end_col = get_initial_indicies()
        car_block = CarBlock(start_row, end_row, start_col, end_col)

        # add each car in the current day to the day's output list
        for car in day[1]:
            car_block.update_block_length(car.seats)

            # get the ranges for this car
            car_block_a1_range = car_block.get_car_block_a1_range()
            heading_a1_range = car_block.get_car_heading_a1_range()
            roles_a1_range = car_block.get_car_roles_a1_range()

            red, green, blue, alpha = get_car_block_colors()

            # prepare all formatting
            car_block_fmt = cellFormat(
                backgroundColor=color(red, green, blue, alpha),
                textFormat=textFormat(fontSize=general_font_size),
            )
            roles_col_fmt = cellFormat(textFormat=textFormat(bold=bold_roles))
            header_row_fmt = cellFormat(textFormat=textFormat(bold=bold_header))

            # add formatting to update list
            day_format.append((car_block_a1_range, car_block_fmt))
            day_format.append((heading_a1_range, header_row_fmt))
            day_format.append((roles_a1_range, roles_col_fmt))

            day_output.append(get_car_output(car, car_block_a1_range, day))

            # move to next writing location
            car_block.move_to_next()

        # batch update minimizes API calls
        ws.batch_update(day_output)
        format_cell_ranges(ws, day_format)


def sort_schedule_for_output(schedule: list) -> list:
    """Sorts each day's cars in the schedule by departure time

        Args:
            schedule:
                a list of days, each day is a list of Car objects

        Returns:
            A list of days, each day's list of Car objects is sorted by their departure time

    """

    # we want to sort each day in the schedule
    for day in schedule:
        # The key parameter in the sort function lets us define the key by which it sorts;
        # in our case, we need it to be the departure time of the cars.
        # We need to access the list of departure times for the current day in the list of
        # the Driver object's days for each car. That's complicated so here's it broken down:
        #
        # 1. day in the schedule: (Day.DayName, [Cars]) <- We want to by sort the list at day[1]
        # 2. Car has a Driver who has a list of Days
        #       - for each car, we need to get the list of the Driver's days
        # 3. We need the times corresponding to the current day
        #       - driver.get_times(Day.DayName) gets us that list (day[0] is a Day.DayName, see 1.)
        # 4. The driver should only have a single departure time, we get that time
        #       - get_times(Day.DayName)[0] is the driver's departure time
        #
        # Putting that all beack together: the sort function sorts by the key provided
        # by the lambda function. The lambda function returns the car's departure time
        # by getting the time from the correct day from the driver
        #
        #

        day[1].sort(key=lambda car: car.driver.get_times(day[0])[0])

    return schedule


def write_to_sheet(schedule: list) -> None:
    """Writes provided schedule to a spreadsheet defined by the provided name.

    An exisiting spreadsheet with the same name will be deleted and a new one will
    be made in its place.
    """
    spreadsheet = create_spreadsheet()

    write_schedule(sort_schedule_for_output(schedule), spreadsheet)
