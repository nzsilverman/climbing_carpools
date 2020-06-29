"""
Backend for reading and writing data with Google Sheets

Reads form responses, dues payers.

Writes cars with drivers and riders

"""


import logging
import gspread
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
this = sys.modules[__name__]

# this is hacky and should be fixed
this.EMAIL_COLUMN = None
this.NAME_COLUMN = None
this.PHONE_COLUMN = None
this.CAR_DESCRIPTION_COLUMN = None
this.SEATS_COLUMN = None
this.IS_RIDER_COLUMN = None
this.IS_DRIVER_COLUMN = None
this.DAYS_INFO_START_COLUMN = None
this.CAR_ROW_SPACING = None


def config_responses():
    """
    Sets configuration for collecting responses
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


def config_output():
    """
    Sets configuration for writing to sheet.
    """

    output = Configuration.config("gform_backend.output")

    this.CAR_ROW_SPACING = output["car_block_spacing"]


def get_dues_payers(dues_sheet):
    """
    Gets the spreadsheet of dues payers
    """

    payers = set()
    for entry in dues_sheet.get_all_records():
        payers.add(entry["Uniqname"].strip())

    return payers


def validate_dues_payers(email, dues_payers):
    """
    Checks if email is a dues payer
    """

    uniqname = email.split("@")[0].strip()
    return uniqname in dues_payers


def parse_location(location):
    """
    Converts location name in value for locations list
    """

    if location == "North Campus (Pierpont Commons)":
        return "NORTH"
    elif location == "Central Campus (The Cube)":
        return "CENTRAL"


def parse_times(time):
    """
    Converts hh:mm to decimal time: hh.(mm/60)
    """

    time = time.split(":")
    print(time)
    return float(time[0]) + (float(time[1]) / 60)


def get_riders(responses, days_enabled, dues_payers):
    """
    Gets riders from the responses
    """

    # list of all riders
    riders = []

    for row in responses[1:]:
        if row[this.IS_RIDER_COLUMN] == "Yes":

            # create rider dictionary
            rider = {
                "name": row[this.NAME_COLUMN],
                "email": row[this.EMAIL_COLUMN],
                "phone": row[this.PHONE_COLUMN],
                "is_dues_paying": validate_dues_payers(
                    row[this.EMAIL_COLUMN], dues_payers
                ),
                "is_driver": False,
                "days": [],
            }

            # assume each day has a locations column and a departure times column
            rider_days_start = this.DAYS_INFO_START_COLUMN

            # create a dict for each day
            for (i, d) in zip(
                range(rider_days_start, rider_days_start + len(days_enabled)),
                days_enabled,
            ):
                day = dict()

                # if climbing this day
                if row[i]:

                    day["day"] = d

                    # add locations
                    day["locations"] = []
                    locations = row[i].split(",")

                    for l in locations:
                        day["locations"].append(parse_location(l.strip()))

                    # add departure times
                    times = row[i + len(days_enabled)].split(",")
                    day["departure_times"] = []

                    for t in times:
                        day["departure_times"].append(parse_times(t.strip()))

                    rider["days"].append(day)

            riders.append(rider)

    return riders


def get_drivers(days_enabled, responses):
    """
    Gets drivers from the responses
    """

    drivers = []

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
                "days": [],
            }

            # assume each day has a locations column and a departure times column
            driver_days_start = this.DAYS_INFO_START_COLUMN + 2 * len(days_enabled)

            # create a dict for each day
            for (i, d) in zip(
                range(driver_days_start, driver_days_start + len(days_enabled)),
                days_enabled,
            ):
                day = dict()

                # if driving this day
                if row[i]:

                    day["day"] = d

                    # add locations
                    day["locations"] = []
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


def members_from_sheet():
    """
    Gets all club members who submitted a response using the form.
    """

    client = AuthorizedClient.get_instance().client

    gform_backend_config = Configuration.config("gform_backend.files")
    days_enabled = Configuration.config("mcc.days_enabled")

    config_responses()

    for sheet in client.openall():
        logger.debug("%s", sheet.title)

    # get responses and dues payers sheets
    responses_sheet = client.open(gform_backend_config["responses_sheet"]).sheet1
    dues_payers_sheet = client.open(gform_backend_config["dues_sheet"]).sheet1

    all_responses = responses_sheet.get_all_values()

    # create lists of riders and drivers
    print(days_enabled)

    riders = get_riders(all_responses, days_enabled, get_dues_payers(dues_payers_sheet))
    drivers = get_drivers(days_enabled, all_responses)

    return riders, drivers


def delete_spreadsheet(name):
    """
    Deletes the spreadsheets in names
    """
    name.strip()

    client = AuthorizedClient.get_instance().client

    for s in client.openall():
        if s.title == name:
            client.del_spreadsheet(s.id)
            logger.info("Deleting spreadsheet: %s", s.title)


def create_spreadsheet():
    """
    Creates a spreadsheet with given name in the location defined by the folder_id.
    The folder_id can be found by viewing the folder in Drive and selecting the 
    id
    
    drive.google.com/../folders/1/<id>
    """

    config = Configuration.config("gform_backend.files")
    client = AuthorizedClient.get_instance().client

    # checks if sheet with name already exists, deletes if exists
    if client.openall(config["output_sheet"]):
        delete_spreadsheet(config["output_sheet"])
        logger.info("Sheet exists, deleting")

    logger.info("Creating sheet")
    spreadsheet = client.create(
        config["output_sheet"], folder_id=config["output_folder_id"]
    )
    spreadsheet.share(
        "rkalnins@umich.edu", notify=False, perm_type="user", role="writer"
    )

    return spreadsheet


def list_spreadsheets():
    """
    Lists spreadsheets available to the client.
    """

    client = AuthorizedClient.get_instance().client

    for s in client.openall():
        print(s.title, s.id)


def unpack_locations(member, day):
    """
    Converts locations in member's locations list to a string of location names
    """

    locations = util.get_day_info_from_member(member, day, "locations")
    location_str = ""

    for l in locations:
        location_str = location_str + l + " "

    return location_str


def unpack_time(driver, day):
    """
    Converts time from decimal time (hh.(mm/60)) to hh:mm format
    """

    time = util.get_day_info_from_member(driver, day, "departure_times")

    # there should only be one time for the driver
    return "{0:02.0f}:{1:02.0f}".format(*divmod(time[0] * 60, 60))


def write_schedule(schedule, spreadsheet):
    """
    Write schedule to provided sheet.
    """

    # each day is a worksheet
    for (i, day) in zip(range(0, len(schedule)), schedule):

        ws = spreadsheet.get_worksheet(i)

        # deletes default Sheet1 and creates a sheet for the current day
        if not ws:
            ws = spreadsheet.add_worksheet(day[0], 100, 100)
        else:
            ws_new = spreadsheet.duplicate_sheet(ws.id, new_sheet_name=day[0])
            spreadsheet.del_worksheet(ws)
            ws = ws_new

        day_output = []

        # track cell indicies for sheet writing ranges

        start_row_index = 1
        start_col_index = 1
        car_start = WSCell(start_row_index, start_col_index)

        end_row_index = 0
        end_col_index = 6
        car_end = WSCell(end_row_index, end_col_index)

        # add each car in the current day to the day's output list
        for car in day[1]:

            # one extra row for the heading, one for the driver
            block_length = car.driver["seats"] + 2

            car_end.inc_row(block_length)
            wsrangeA1 = WSRange(car_start, car_end).getA1()

            # cell format
            ws.format(
                wsrangeA1,
                {
                    "backgroundColor": {
                        "red": uniform(0.5, 1.0),
                        "green": uniform(0.5, 1.0),
                        "blue": uniform(0.5, 1.0),
                        "alpha": 0.5,
                    }
                },
            )

            # add headings and driver
            car_output = {
                "range": wsrangeA1,
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

            # add rider info
            for r in car.riders:
                car_output["values"].append(
                    [
                        "Rider",
                        r["name"],
                        "",
                        r["phone"],
                        "",
                        unpack_locations(r, day[0]),
                    ]
                )

            day_output.append(car_output)

            # move to next writing location
            car_start.inc_row(this.CAR_ROW_SPACING + block_length)
            car_end.inc_row(this.CAR_ROW_SPACING)

        # batch update minimizes API calls
        ws.batch_update(day_output)


def write_to_sheet(schedule):
    """
    Writes provided schedule to a spreadsheet defined by the provided name.
    An exisiting spreadsheet with the same name will be deleted and a new one will
    be made in its place.
    """
    config_output()
    spreadsheet = create_spreadsheet()
    write_schedule(schedule, spreadsheet)
