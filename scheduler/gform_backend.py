import logging
import gspread
import pandas as pd
import json
import util
import datetime
from random import uniform

from classes.AuthorizedClient import AuthorizedClient
from classes.WSCell import WSCell
from classes.WSRange import WSRange


logger = logging.getLogger(__name__)

NAME_COLUMN = 2
EMAIL_COLUMN = 1
PHONE_COLUMN = 3
SEATS_COLUMN = 6
CAR_DESCRIPTION_COLUMN = 5
DAYS_INFO_START_COLUMN = 7

CAR_ROW_SPACING = 4

OUTPUT_TESTING_FOLDER_ID = "1j1w_0k5bIgqxJfmQmxbZZoGr66fJT4Y4"


def get_dues_payers(dues_sheet):
    payers = set()
    for entry in dues_sheet.get_all_records():
        payers.add(entry["Uniqname"].strip())

    return payers


def validate_dues_payers(email, dues_payers):
    uniqname = email.split("@")[0].strip()
    return uniqname in dues_payers


def parse_location(location):
    if location == "North Campus (Pierpont Commons)":
        return "NORTH"
    elif location == "Central Campus (The Cube)":
        return "CENTRAL"


def parse_times(time):
    time = time.split(":")
    return float(time[0]) + (float(time[1]) / 60)


def get_riders(responses, days_enabled, dues_payers):
    riders = []

    for row in responses[1:]:
        if row[4] == "Rider":
            rider = {
                "name": row[NAME_COLUMN],
                "email": row[EMAIL_COLUMN],
                "phone": row[PHONE_COLUMN],
                "is_dues_paying": validate_dues_payers(row[2], dues_payers),
                "is_driver": False,
                "days": [],
            }

            # assume each day has a locations column and a departure times column

            rider_days_start = DAYS_INFO_START_COLUMN
            for (i, d) in zip(
                range(rider_days_start, rider_days_start + len(days_enabled)),
                days_enabled,
            ):
                day = dict()

                # if climbing this day
                if row[i]:

                    day["day"] = d
                    day["locations"] = []
                    locations = row[i].split(",")

                    for l in locations:
                        day["locations"].append(parse_location(l.strip()))

                    times = row[i + len(days_enabled)].split(",")
                    day["departure_times"] = []

                    for t in times:
                        day["departure_times"].append(parse_times(t.strip()))

                    rider["days"].append(day)

            riders.append(rider)

    return riders


def get_drivers(days_enabled, responses):
    drivers = []

    for row in responses[1:]:
        if row[4] == "Driver":
            driver = {
                "name": row[NAME_COLUMN],
                "email": row[EMAIL_COLUMN],
                "phone": row[PHONE_COLUMN],
                "car_type": row[CAR_DESCRIPTION_COLUMN],
                "seats": int(row[SEATS_COLUMN]),
                "is_dues_paying": True,
                "is_driver": True,
                "days": [],
            }

            # assume each day has a locations column and a departure times column

            driver_days_start = DAYS_INFO_START_COLUMN + 2 * len(days_enabled)
            for (i, d) in zip(
                range(driver_days_start, driver_days_start + len(days_enabled)),
                days_enabled,
            ):
                day = dict()

                # if driving this day
                if row[i]:

                    day["day"] = d
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


def members_from_sheet(dues_payers, responses, days_enabled):
    """
    Gets all club members who submitted a response using the form.
    """

    client = AuthorizedClient.get_instance().client

    for sheet in client.openall():
        logger.debug("%s", sheet.title)

    responses_sheet = client.open(responses).sheet1
    dues_payers_sheet = client.open(dues_payers).sheet1

    all_responses = responses_sheet.get_all_values()

    riders = get_riders(all_responses, days_enabled, get_dues_payers(dues_payers_sheet))
    drivers = get_drivers(days_enabled, all_responses)

    return riders, drivers


def clear_testing_output(names):
    for n in names:
        n.strip()

    client = AuthorizedClient.get_instance().client
    for s in client.openall():
        if s.title in names:
            client.del_spreadsheet(s.id)


def create_spreadsheet(name, location, client):

    if not client.openall(name):
        logger.info("Creating sheet")
        spreadsheet = client.create(name, folder_id=location)
        spreadsheet.share(
            "rkalnins@umich.edu", notify=False, perm_type="user", role="writer"
        )
    else:
        logger.info("Sheet exists")
        spreadsheet = client.open(name)

    return spreadsheet


def list_spreadsheets():
    client = AuthorizedClient.get_instance().client

    for s in client.openall():
        print(s.title, s.id)


def unpack_locations(member, day):
    locations = util.get_day_info_from_member(member, day, "locations")
    location_str = ""

    for l in locations:
        location_str = location_str + l + " "

    return location_str


def unpack_time(driver, day):
    time = util.get_day_info_from_member(driver, day, "departure_times")

    # there should only be one time for the driver
    return "{0:02.0f}:{1:02.0f}".format(*divmod(time[0] * 60, 60))


def write_schedule(schedule, spreadsheet):

    for (i, day) in zip(range(0, len(schedule)), schedule):
        print(day[0])

        ws = spreadsheet.get_worksheet(i)

        if not ws:
            ws = spreadsheet.add_worksheet(day[0], 100, 100)
        else:
            ws_new = spreadsheet.duplicate_sheet(ws.id, new_sheet_name=day[0])
            spreadsheet.del_worksheet(ws)
            ws = ws_new

        day_output = []

        start_row_index = 1
        start_col_index = 1
        car_start = WSCell(start_row_index, start_col_index)

        end_row_index = 0
        end_col_index = 5
        car_end = WSCell(end_row_index, end_col_index)

        for car in day[1]:
            print("Driver:", car.driver["name"])
            # one extra row for the heading, one for the driver
            block_length = car.driver["seats"] + 2

            car_end.inc_row(block_length)
            wsrangeA1 = WSRange(car_start, car_end).getA1()

            print(wsrangeA1)

            ws.format(
                wsrangeA1,
                {
                    "backgroundColor": {
                        "red": uniform(0.5, 1.0),
                        "green": uniform(0.5, 1.0),
                        "blue": uniform(0.5, 1.0),
                        "alpha": 0.5,
                    }
                }
            )

            car_output = {
                "range": wsrangeA1,
                "values": [
                    ["", "Name", "Phone Number", "Departure Time", "Locations"],
                    [
                        "Driver",
                        car.driver["name"],
                        car.driver["phone"],
                        unpack_time(car.driver, day[0]),
                        unpack_locations(car.driver, day[0]),
                    ],
                ],
            }

            for r in car.riders:
                car_output["values"].append(
                    ["Rider", r["name"], r["phone"], "", unpack_locations(r, day[0])]
                )

            day_output.append(car_output)

            print(car_output)

            car_start.inc_row(CAR_ROW_SPACING + block_length)
            car_end.inc_row(CAR_ROW_SPACING)

        ws.batch_update(day_output)


def write_to_sheet(schedule, spreadsheet_name):
    client = AuthorizedClient.get_instance().client

    spreadsheet = create_spreadsheet(spreadsheet_name, OUTPUT_TESTING_FOLDER_ID, client)

    write_schedule(schedule, spreadsheet)
