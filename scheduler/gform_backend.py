"""Backend for reading and writing data with Google Sheets/

Reads form responses and due paying members sheet.
Writes cars with drivers and riders

Typical usage:
    import gform_backend
    <call appropriate function>

"""

import logging
import gspread
from gspread_formatting import *
import json
import sys
import datetime
from random import uniform

import scheduler.util as util
from scheduler.classes.AuthorizedClient import AuthorizedClient
from scheduler.classes.WSCell import WSCell
from scheduler.classes.WSRange import WSRange
from scheduler.classes.Configuration import Configuration

logger = logging.getLogger(__name__)
this = sys.modules[__name__] # TODO -> I am confused by this (nathan)

# TODO -> why is the 'this' keyword being used here? I see it is using the modules
# this is hacky and should be fixed
this.EMAIL_COLUMN: int = None
this.NAME_COLUMN: int = None
this.PHONE_COLUMN: int = None
this.CAR_DESCRIPTION_COLUMN: int = None
this.SEATS_COLUMN: int = None
this.IS_RIDER_COLUMN: int = None
this.IS_DRIVER_COLUMN: int = None
this.DAYS_INFO_START_COLUMN: int = None
this.CAR_ROW_SPACING: int = None


def config_responses():
    """Sets configuration needed for collecting responses.

    Uses configuration data found in the config files for this information
    """

    columns = Configuration.config("gform_backend.columns")

    this.EMAIL_COLUMN = columns["email"]
    this.NAME_COLUMN = columns["name"]
    this.PHONE_COLUMN = columns["phone_number"]
    this.CAR_DESCRIPTION_COLUMN = columns["car_type"]
    this.SEATS_COLUMN = columns["seats"]
    this.IS_RIDER_COLUMN = columns["is_rider"]
    this.IS_DRIVER_COLUMN = columns["is_driver"]
    this.DAYS_INFO_START_COLUMN = columns["days_info_start"]


def get_dues_payers(dues_sheet: str) -> set:
    """Gets the spreadsheet of dues payers.

        Args:
            dues_sheet:
                A string object that contains all the data from the due paying members spreadhset
        
        Returns:
            A set that contains uniqnames of all due paying members
    """

    payers = set()
    for entry in dues_sheet.get_all_records():
        payers.add(entry["Uniqname"].strip())

    return payers

# TODO -> why is dues_payers type str and above we made a set for due paying members?
def validate_dues_payers(email: str, dues_payers: str) -> bool:
    """Checks if email is a dues payer.

        Args:
            email:
                string of an email that contains a uniqname. Uniqname is defined as the 
                email address before the @ symbol
            dues_payers:
                String of dues payers
        
        Returns:
            True -> email address paid dues
            False -> email address did not pay dues
    """

    uniqname = email.split("@")[0].strip()
    return uniqname in dues_payers


def parse_location(location: str) -> str:
    """Converts location name in value for locations list.

        Args:
            location: 
                string that contains the location
        Returns
            String that is either "NORTH" or "CENTRAL"
    """

    if location == "North Campus (Pierpont Commons)":
        return "NORTH"
    elif location == "Central Campus (The Cube)":
        return "CENTRAL"


def parse_times(time: str) -> float:
    """Converts hh:mm to decimal time: hh.(mm/60).

        Args:
            time:
                time, as a string in hh:mm time
        
        Returns
            float that is the time converted to hh.(mm/60) time
    """

    time = time.split(":")
    return float(time[0]) + (float(time[1]) / 60)


def get_riders(responses: list, days_enabled: list, dues_payers: set) -> list:
    """Creates a list of riders from the responses.

        Args:
            responses:
                list of responses from spreadsheet
            days_enabled:
                list of days that the spreadsheet software is run for
            dues_payers:
                set of due paying members
        
        Returns:
            list of riders, where each entry is a rider dictionary entry


    """

    # list of all riders
    riders = list()

    for row in responses[1:]:
        if row[this.IS_RIDER_COLUMN] == "Yes":

            # create rider dictionary
            rider = {
                "name":
                    row[this.NAME_COLUMN],
                "email":
                    row[this.EMAIL_COLUMN],
                "phone":
                    row[this.PHONE_COLUMN],
                "is_dues_paying":
                    validate_dues_payers(row[this.EMAIL_COLUMN], dues_payers),
                "is_driver":
                    False,
                "days":
                    list(),
            }

            # assume each day has a locations column and a departure times column
            rider_days_start = this.DAYS_INFO_START_COLUMN

            # create a dict for each day
            # TODO -> need some more clarity for this zip range shenanigan
            for (i, d) in zip(
                    range(rider_days_start,
                          rider_days_start + len(days_enabled)),
                    days_enabled,
            ):
                day = dict()

                # if climbing this day
                if row[i]:

                    day["day"] = d

                    # add locations
                    day["locations"] = list()
                    locations = row[i].split(",")

                    for l in locations:
                        day["locations"].append(parse_location(l.strip()))

                    # add departure times
                    times = row[i + len(days_enabled)].split(",")
                    day["departure_times"] = list()

                    for t in times:
                        day["departure_times"].append(parse_times(t.strip()))

                    rider["days"].append(day)

            riders.append(rider)

    return riders


# TODO -> this is a lot of somewhat unclear code that is repeated from above.
# I would suggest we combine the reading of drivers and riders and do it in one
# pass over the data.

def get_drivers(responses: list, days_enabled: list) -> list:
    """Gets drivers from the responses.

        Args:
            responses:
                list of responses from spreadsheet
            days_enabled:
                list of days that the spreadsheet software is run for
        
        Returns:
            list of drivers, where each entry is a driver dictionary entry
    """

    drivers = list()

    for row in responses[1:]:
        if row[this.IS_DRIVER_COLUMN] == "Yes":

            # create driver dictionary
            driver = {
                "name": row[this.NAME_COLUMN],
                "email": row[this.EMAIL_COLUMN],
                "phone": row[this.PHONE_COLUMN],
                "car_type": row[this.CAR_DESCRIPTION_COLUMN],
                "seats": int(row[this.SEATS_COLUMN]),
                "is_dues_paying": True,
                "is_driver": True,
                "days": list(),
            }

            # assume each day has a locations column and a departure times column
            driver_days_start = this.DAYS_INFO_START_COLUMN + 2 * len(
                days_enabled)

            # create a dict for each day
            for (i, d) in zip(
                    range(driver_days_start,
                          driver_days_start + len(days_enabled)),
                    days_enabled,
            ):
                day = dict()

                # if driving this day
                if row[i]:

                    day["day"] = d

                    # add locations
                    day["locations"] = list()
                    locations = row[i].split(",")

                    for l in locations:
                        day["locations"].append(parse_location(l.strip()))

                    # driver only has one departure time
                    day["departure_times"] = [
                        parse_times(row[i + len(days_enabled)].split(",")[0])
                    ]

                    driver["days"].append(day)

            drivers.append(driver)

    return drivers


def members_from_sheet() -> (list, list):
    """Gets all club members who submitted a response using the form.

        Returns:
            (list, list)
            The list in index 0 is a list of riders, where each entry is a rider dict
            The list in index 1 is a list of drivers, where each entry is a driver dict
    """

    client = AuthorizedClient.get_instance().client

    gform_backend_config = Configuration.config("gform_backend.files")
    days_enabled = Configuration.config("mcc.days_enabled")

    config_responses()

    for sheet in client.openall():
        logger.debug("%s", sheet.title)

    # get responses and dues payers sheets
    responses_sheet = client.open(
        gform_backend_config["responses_sheet"]).sheet1
    dues_payers_sheet = client.open(gform_backend_config["dues_sheet"]).sheet1

    all_responses = responses_sheet.get_all_values()

    # create lists of riders and drivers
    print(days_enabled)

    riders = get_riders(all_responses, days_enabled,
                        get_dues_payers(dues_payers_sheet))
    drivers = get_drivers(all_responses, days_enabled)

    return riders, drivers


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
                                folder_id=config["output_folder_id"])
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


def unpack_locations(member: dict, day: str) -> str:
    """Converts locations in member's locations list to a string of location names

        Appends together all of the location strings for a particular member

        Args:
            member:
                dictionary entry of a member
            day:
                string of which day to query on
        
        Returns:
            string that is a concatenated string of all the locations a member is trying to leave from
    """

    locations = util.get_day_info_from_member(member, day, "locations")
    location_str = ""

    for l in locations:
        location_str = location_str + l + " "

    return location_str


def unpack_time(driver: dict, day: str) -> str:
    """Converts time from decimal time (hh.(mm/60)) to hh:mm format

        Args:
            driver:
                dictionary entry of the driver
            day:
                day to use
        
        Returns:
            Returns the unpacked time as a string, converted from (hh.(mm/60)) to (hh:mm) format
    """

    time = util.get_day_info_from_member(driver, day, "departure_times")

    # there should only be one time for the driver
    return "{0:02.0f}:{1:02.0f}".format(*divmod(time[0] * 60, 60))


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


# TODO -> This function is a monster. I appreciate that it works well, but I think for maintainability it should
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

    notes_enabled = output_config["notes_column"]
    car_block_spacing = output_config["car_block_spacing"]
    column_buffer_left = output_config["column_buffer_left"]
    row_buffer_top = output_config["row_buffer_top"]
    bold_header = output_config["bold_header"]
    bold_roles = output_config["bold_roles"]
    sheet_name_base = output_config["name"]
    name_suffix_list = output_config["name_suffixes"]
    use_sheet_titles = output_config["use_sheet_titles"]
    bold_title = output_config["bold_title"]
    title_font_size = output_config["title_font_size"]
    title_cell_merge_count = output_config["title_cell_merge_count"]

    general_font_size = output_config["general_font_size"]
    column_widths = output_config["column_widths"]
    defualt_width = output_config["default_width"]

    # each day is a worksheet (i.e. a tab)
    for (i, day) in zip(range(0, len(schedule)), schedule):
        ws = spreadsheet.get_worksheet(i)

        # TODO -> would like more of an explanation of this if statement 
        # deletes default Sheet1 and creates a sheet for the current day
        if not ws:
            ws = spreadsheet.add_worksheet(day[0], 100, 100)
        else:
            ws_new = spreadsheet.duplicate_sheet(ws.id, new_sheet_name=day[0])
            spreadsheet.del_worksheet(ws)
            ws = ws_new

        day_output = list()
        days_format = list()
        widths_list = list()

        # TODO -> needs more of a comment for what this is acheiving
        for j, w in zip(range(1, len(column_widths) + 1), column_widths):
            col_lettr = WSCell(1, j).get_column()

            if i == len(column_widths):
                col_lettr = col_lettr + ":"

            widths_list.append((col_lettr, w))

        set_column_widths(ws, widths_list)

        # TODO -> more comments please
        # sheet titles
        if use_sheet_titles:
            title_range_a1 = WSRange(WSCell(1, 1),
                                     WSCell(1, title_cell_merge_count)).getA1()

            cell_A1A1 = WSRange(WSCell(1, 1), WSCell(1, 1)).getA1()

            title = sheet_name_base + name_suffix_list[i]
            heading_text = {
                "range": cell_A1A1,
                "values": [[title]],
            }

            title_fmt = cellFormat(textFormat=textFormat(
                bold=bold_title, fontSize=title_font_size))

            day_output.append(heading_text)
            days_format.append((cell_A1A1, title_fmt))
            ws.merge_cells(title_range_a1)

        # TODO -> comments/ explanations of what this is doing, like why we track cell indicies and where
        # the magic numbers come from

        # track cell indicies for sheet writing ranges
        if use_sheet_titles:
            start_row_index = 1
        else:
            start_row_index = 0

        start_row_index += row_buffer_top
        start_col_index = 1 + column_buffer_left

        end_row_index = row_buffer_top
        if notes_enabled:
            end_col_index = start_col_index + 6
        else:
            end_col_index = start_col_index + 5

        # corners of each block
        car_block_upper_left = WSCell(start_row_index, start_col_index)
        car_block_upper_right = WSCell(start_row_index, end_col_index)
        car_block_lower_right = WSCell(end_row_index, end_col_index)
        car_block_lower_left = WSCell(end_row_index, start_col_index)

        # add each car in the current day to the day's output list
        for car in day[1]:

            # one extra row for the heading, one for the driver
            block_length = car.driver["seats"] + 2

            car_block_lower_right.inc_row(block_length)
            car_block_lower_left.inc_row(block_length)

            car_block_a1_range = WSRange(car_block_upper_left,
                                         car_block_lower_right).getA1()

            heading_a1_range = WSRange(car_block_upper_left,
                                       car_block_upper_right).getA1()

            roles_a1_range = WSRange(car_block_upper_left,
                                     car_block_lower_left).getA1()

            red, green, blue, alpha = get_car_block_colors()

            car_block_fmt = cellFormat(
                backgroundColor=color(red, green, blue, alpha),
                textFormat=textFormat(fontSize=general_font_size),
            )

            roles_col_fmt = cellFormat(textFormat=textFormat(bold=bold_roles))

            header_row_fmt = cellFormat(textFormat=textFormat(bold=bold_header))

            days_format.append((car_block_a1_range, car_block_fmt))
            days_format.append((heading_a1_range, header_row_fmt))
            days_format.append((roles_a1_range, roles_col_fmt))

            # add headings and driver
            car_output = {
                "range":
                    car_block_a1_range,
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
                        car.driver["name"],
                        car.driver["car_type"],
                        car.driver["phone"],
                        unpack_time(car.driver, day[0]),
                        unpack_locations(car.driver, day[0]),
                    ],
                ],
            }

            if notes_enabled:
                car_output["values"][0].append("Notes")
                car_output["values"][1].append("")

            # add rider info
            for r in car.riders:
                row = [
                    "Rider",
                    r["name"],
                    "",
                    r["phone"],
                    "",
                    unpack_locations(r, day[0]),
                ]

                if notes_enabled:
                    row.append("")

                car_output["values"].append(row)

            day_output.append(car_output)

            # move to next writing location
            car_block_upper_left.inc_row(car_block_spacing + block_length)
            car_block_upper_right.inc_row(car_block_spacing + block_length)

            # update in the beginning of the loop when block size is calculated
            car_block_lower_right.inc_row(car_block_spacing)
            car_block_lower_left.inc_row(car_block_spacing)

        # batch update minimizes API calls
        ws.batch_update(day_output)
        format_cell_ranges(ws, days_format)


def write_to_sheet(schedule: list) -> None:
    """Writes provided schedule to a spreadsheet defined by the provided name.

    An exisiting spreadsheet with the same name will be deleted and a new one will
    be made in its place.
    """
    spreadsheet = create_spreadsheet()
    write_schedule(schedule, spreadsheet)
