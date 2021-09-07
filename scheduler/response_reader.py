import logging

import gspread

import scheduler.classes.Day as Day
import scheduler.classes.MeetingLocation as MeetingLocation
from scheduler.classes.AuthorizedClient import AuthorizedClient
from scheduler.classes.Configuration import Configuration
from scheduler.classes.Driver import Driver
from scheduler.classes.Rider import Rider

logger = logging.getLogger(__name__)


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


def validate_dues_payers(email: str, dues_payers: set) -> bool:
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


def parse_location(location: str) -> MeetingLocation:
    """Converts location name in value for locations list.

        Args:
            location:
                string that contains the location
        Returns
            String that is either "NORTH" or "CENTRAL"
    """

    if location == "North Campus (Pierpont Commons)":
        return MeetingLocation.MeetingLocation.NORTH
    elif location == "Central Campus (The Cube)":
        return MeetingLocation.MeetingLocation.CENTRAL


def parse_times(time: str) -> float:
    """Converts hh:mm to decimal time: hh.(mm/60).

        Args:
            time:
                time, as a string in hh:mm <AM|PM> time

        Returns
            float that is the time converted to hh.(mm/60) time
    """
    time = time.split()

    # conversion from 12-hr with AM/PM time to 24-hr time
    if time[1] == "PM":
        conversion_scalar = 12
    else:
        conversion_scalar = 0

    time = time[0].split(":")
    return float(time[0]) + (float(time[1]) / 60) + conversion_scalar


def get_days_and_locations(start_col: int, response: list,
                           days_enabled: list) -> list:
    """Converts club member responses regarding driving and riding times and departure locations
    from the Google Form responses sheet into DayInfo objects

        Args:
            start_col:
                column where this response's time and locations begin
            response:
                a list of all values in a carpool form response's row
            days_enabled:
                a list of days for which the scheduler is scheduling

        Returns
            a list of DayInfo objects corresponding to the provided carpool form response


        Typical Usage:
            rider = Rider(
                name=row[name_column],
                email=row[email_column],
                phone=row[phone_column],
                is_dues_paying=validate_dues_payers(row[email_column],
                                                    dues_payers),
                days=get_days_and_locations(days_info_start_column, row,
                                            days_enabled))


     assume each day has a locations column and a departure times column

     n = days_enabled


     This diagram is a representation of the Google Form responses sheet showing from which
     columns data is being extracted. Day 1 Locations Rider is the first column of
     location data if the member is a rider (column I of the current v2.0.0 responses sheet).

                 (start rider iter here)  (end rider iter here)  (start driver iter here)                 (end driver iter here)
                 DAYS_INFO_START                            |    driver_days_start                            |
                    |                                       |         |                                       |
                    V                                       V         V                                       V
             |   | Day 1     |   | Day n     | Day 1 |   | Day n | Day 1     |   | Day n     | Day 1  |   | Day n  |
             |   | Locations |...| Locations | Times |...| Times | Locations |...| Locations | Times  |...| Times  |
             |   | Rider     |   | Rider     | Rider |   | Rider | Driver    |   | Driver    | Driver |   | Driver |
     --------|...|-----------|---|-----------|-------|---|-------|-----------|---|-----------|--------|---|--------|
     Member 1|   |           |   |           |       |   |       |           |   |           |        |   |        |
     Member 2|   |
     .       |   |
     .       |   |
     .       |   |
     Member n|   |
    """

    # create a dict for each day

    days = list()

    for (i, d) in zip(
            range(start_col, start_col + len(days_enabled)),
            days_enabled,
    ):

        # if driving this day
        if response[i]:

            times_strs = response[i + len(days_enabled)].split(",")

            day = Day.DayInfo(day=Day.from_str(d),
                              times=[
                                  parse_times(times_strs[i])
                                  for i in range(0, len(times_strs))
                              ],
                              locations=list())

            locations = response[i].split(",")

            for l in locations:
                day.locations.append(parse_location(l.strip()))

            days.append(day)

    return days


def get_riders_and_drivers(
        responses: list, days_enabled: list,
        dues_payers_sheet: gspread.models.Worksheet) -> (list, list):
    """Gets drivers from the responses.

        Args:
            responses:
                list of responses from spreadsheet
            days_enabled:
                list of days that the spreadsheet software is run for

        Returns
            tuple of lists
                list at index 0: list of Driver objects
                list at index 1: list of Rider objects
    """

    dues_payers = get_dues_payers(dues_payers_sheet)

    drivers = list()
    riders = list()

    columns = Configuration.config("gform_backend.columns")

    name_column = columns["name"]
    email_column = columns["email"]
    phone_column = columns["phone_number"]
    car_type_column = columns["car_type"]
    seats_column = columns["seats"]
    is_rider_column = columns["is_rider"]
    is_driver_column = columns["is_driver"]
    days_info_start_column = columns["days_info_start"]

    for row in responses[1:]:
        is_driver = (row[is_driver_column] == "Yes")
        is_rider = (row[is_rider_column] == "Yes")

        if is_driver:

            driver = Driver(name=row[name_column],
                            email=row[email_column],
                            phone=row[phone_column],
                            is_dues_paying=validate_dues_payers(
                                row[email_column], dues_payers),
                            days=get_days_and_locations(
                                days_info_start_column + 2 * len(days_enabled),
                                row, days_enabled),
                            car_type=row[car_type_column],
                            seats=int(row[seats_column]))

            for d in driver.days:
                logger.debug("[Driver] %s: %s", driver.name, d)

            drivers.append(driver)

        if is_rider:

            rider = Rider(name=row[name_column],
                          email=row[email_column],
                          phone=row[phone_column],
                          is_dues_paying=validate_dues_payers(
                              row[email_column], dues_payers),
                          days=get_days_and_locations(days_info_start_column,
                                                      row, days_enabled))

            for d in rider.days:
                logger.debug("[Rider] %s: %s", rider.name, d)

            riders.append(rider)

    return riders, drivers


def members_from_sheet() -> (list, list):
    """Gets all club members who submitted a response using the form.

        Returns:
            (list, list)
            The list in index 0 is a list of riders, where each entry is a Rider object
            The list in index 1 is a list of drivers, where each entry is a Driver object
    """

    client = AuthorizedClient.get_instance().client

    gform_backend_config = Configuration.config("gform_backend.files")
    days_enabled = Configuration.config("mcc.days_enabled")

    for sheet in client.openall():
        logger.debug("%s", sheet.title)

    # get responses and dues payers sheets
    responses_sheet = client.open_by_key(
        gform_backend_config["responses_sheet"]).sheet1
    dues_payers_sheet = client.open_by_key(
        gform_backend_config["dues_sheet"]).sheet1

    all_responses = responses_sheet.get_all_values()

    # create lists of riders and drivers
    print(days_enabled)

    return get_riders_and_drivers(all_responses, days_enabled,
                                  dues_payers_sheet)
