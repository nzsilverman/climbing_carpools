from __future__ import print_function
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

def generate_response_lists():
    """Return lists of drivers and riders from google form."""

    SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    SECRETS_FILE = "secret.json"
    SPREADSHEET = "Carpool Scheduling Template (Responses)"
    DUES_SHEET = "Due Paying Members"
    # Based on docs here - http://gspread.readthedocs.org/en/latest/oauth2.html
    # Load in the secret JSON key (must be a service account)
    json_key = json.load(open(SECRETS_FILE))
    # Authenticate using the signed key
    # credentials = SignedJwtAssertionCredentials(json_key['client_email'],
    #                                             json_key['private_key'], SCOPE)
    credentials = ServiceAccountCredentials.from_json_keyfile_name('secret.json', SCOPE)

    gc = gspread.authorize(credentials)
    # print("The following sheets are available")
    # for sheet in gc.openall():
    #     print("{} - {}".format(sheet.title, sheet.id))
    # Open up the workbook based on the spreadsheet name
    spreadsheet = gc.open(SPREADSHEET)
    # Get the first sheet
    sheet = spreadsheet.sheet1
    # Extract all data into a dataframe


    # data = sheet.get_all_records() # old version, uses a dict
    data = sheet.get_all_values() # Reads in as a list of lists, doesn't combine dict entries


    # print data in sheet
    # for item in data:
    #     print(item)
    #     print('Len: {}'.format(len(item)))
    #     print('\n')

    # Get due paying members list
    dues_sheet = gc.open(DUES_SHEET).sheet1.get_all_records()
    # uniquenames of people who have paid dues
    dues_list = []
    for entry in dues_sheet:
        dues_list.append(entry["Uniquename"])

    # Declaration of lists that will be populated
    tues_drivers = []
    tues_riders = []
    thurs_drivers = []
    thurs_riders = []
    sun_drivers = []
    sun_riders = []

    # Read every row of input data. Row 0 is the titles
    for row in data[1:]:
        email = row[1]
        name = row[2]

        # Create tuesday dict
        tues = {}
        tues['email'] = email
        tues['name'] = name
        tues['type'] = row[3]
        tues['driver_departure'] = row[4]
        tues['driver_num_riders'] = row[5]
        tues['rider_departure'] = row[6]
        tues['departure_time'] = row[7]
        tues['alt_time'] = row[8]

        # Create thursday dict
        thurs = {}
        thurs['email'] = email
        thurs['name'] = name
        thurs['type'] = row[9]
        thurs['driver_departure'] = row[10]
        thurs['driver_num_riders'] = row[11]
        thurs['rider_departure'] = row[12]
        thurs['departure_time'] = row[13]
        thurs['alt_time'] = row[14]

        # Create sunday dict
        sun = {}
        sun['email'] = email
        sun['name'] = name
        sun['type'] = row[15]
        sun['driver_departure'] = row[16]
        sun['driver_num_riders'] = row[17]
        sun['rider_departure'] = row[18]

        # Validate tuesday has all necesary fields and if they are a rider, they
        # have paid dues
        # import pdb; pdb.set_trace()
        if tues['type'] == 'Driver':
            # check appropriate fields are non empty
            if tues['driver_departure'] and tues['driver_num_riders'] and tues['departure_time']:
                # check departure time is 7:30 or alternate time provided
                if tues['departure_time'] != '7:30 pm':
                    if tues['alt_time']:
                        tues_drivers.append(tues)
                else:
                    tues_drivers.append(tues)
        elif tues['type'] == 'Rider':
            # Rider case
            uniquename = tues['email'].split('@')[0].strip()
            if tues['rider_departure'] and tues['departure_time']:
                # Make sure they have paid dues
                if uniquename in dues_list:
                    tues_riders.append(tues)

        # Validate thursday has all necesary fields and if they are a rider, they
        # have paid dues
        if thurs['type'] == 'Driver':
            # check appropriate fields are non empty
            if thurs['driver_departure'] and thurs['driver_num_riders'] and thurs['departure_time']:
                # check departure time is 7:30 or alternate time provided
                if thurs['departure_time'] != '7:30 pm':
                    if thurs['alt_time']:
                        thurs_drivers.append(thurs)
                else:
                    thurs_drivers.append(thurs)
        elif thurs['type'] == 'Rider':
            # Rider case
            uniquename = thurs['email'].split('@')[0].strip()
            if thurs['rider_departure'] and thurs['departure_time']:
                # Make sure they have paid dues
                if uniquename in dues_list:
                    thurs_riders.append(thurs)


        # Validate sunday has all necesary fields and if they are a rider, they
        # have paid dues
        if sun['type'] == 'Driver':
            # check appropriate fields are non empty
            if sun['driver_departure'] and sun['driver_num_riders']:
                sun_drivers.append(sun)
        elif sun['type'] == 'Rider':
            # Rider case
            uniquename = sun['email'].split('@')[0].strip()
            if sun['rider_departure']:
                # Make sure they have paid dues
                if uniquename in dues_list:
                    sun_riders.append(sun)
    return (tues_drivers, tues_riders, thurs_drivers, thurs_riders, sun_drivers, sun_riders)
    # Debug printing
    # print("tues_drivers")
    # print(tues_drivers)
    #
    # print("tues_riders")
    # print(tues_riders)
    #
    # print("thurs_drivers")
    # print(thurs_drivers)
    #
    # print("thurs_riders")
    # print(thurs_riders)

    # print("sun_drivers")
    # print(sun_drivers)
    #
    # print("sun_riders")
    # print(sun_riders)
