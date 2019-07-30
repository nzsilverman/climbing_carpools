from __future__ import print_function
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

from classes.Loc import Loc
from classes.Dept_Time import Dept_Time
from classes.Driver import Driver
from classes.Rider import Rider

def get_responses_from_spreadsheet(spreadsheet_name, dues_sheet_name):
    """ Returns a tuple of spreadsheet data as a 2D list and the dues sheet. """

    # Use Google Developer API to read spreadsheet
    # Based on docs here - http://gspread.readthedocs.org/en/latest/oauth2.html
    SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    SECRETS_FILE = "secret.json"
    SPREADSHEET = spreadsheet_name 
    DUES_SHEET = dues_sheet_name 
    # Load in the secret JSON key (must be a service account)
    json_key = json.load(open(SECRETS_FILE))
    # Authenticate using the signed key
    credentials = ServiceAccountCredentials.from_json_keyfile_name('secret.json', SCOPE)

    gc = gspread.authorize(credentials)

    # Debugging printing of all available google sheets
    # print("The following sheets are available")
    # for sheet in gc.openall():
    #     print("{} - {}".format(sheet.title, sheet.id))

    # Open up the workbook based on the spreadsheet name
    spreadsheet = gc.open(SPREADSHEET)

    # Get the first sheet
    sheet = spreadsheet.sheet1

    # Extract all data into a dataframe
    data = sheet.get_all_values() # Reads in as a list of lists, doesn't combine dict entries
    
    # Get due paying members list
    dues_sheet = gc.open(DUES_SHEET).sheet1.get_all_records()
    # Put uniquenames of people who have paid dues into a list
    dues_list = []
    for entry in dues_sheet:
        dues_list.append(entry["Uniquename"])

    return (data, dues_list)

def create_lists(sheet_name, dues_sheet_name):
    
    # Get Data and Dues List
    responses = get_responses_from_spreadsheet(sheet_name, dues_sheet_name)
    data = responses[0]
    dues_list = responses[1]

    # Declaration of lists that will be populated
    tues_drivers = []
    tues_riders = []
    thurs_drivers = []
    thurs_riders = []
    sun_drivers = []
    sun_riders = []

    # Read every row of input data. Row 0 is the titles
    for row in data[1:]:
        # Timestamp is the 0th element in the row
        email = row[1]
        name = row[2]

        # Splice array, entries [3,9) are for tuesday
        tues_array = row[3:9]
        
        # Format of Data for Tuesday and Thursday
        # [0] type
        # [1] driver_departure
        # [2] driver_num_riders
        # [3] rider_departure
        # [4] departure_time
        # [5] alt_time

        # Create Tuesday Entry
        member_type = tues_array[0]
        if member_type == "Driver":
            # Driver Type

            # TODO FINISH THIS

            tues_driver = get_driver(tues_array)
        elif member_type == "Rider":
            # Rider Type


        driver_departure =      row[4]
        driver_num_riders =     row[5]
        rider_departure =       row[6]
        dept_time =             row[7]
        alt_time =              row[8]
         
        if driver_departure == "Exclusively departing from North campus":
            # Only North
            loc = Loc.NORTH
        elif driver_departure == "Leaving from North and going to Central to pickup riders":
            # Both
            loc = Loc.NORTH_AND_CENTRAL
        elif driver.departure == "Exclusively departing from Central campus":
            # Only central
            loc = Loc.CENTRAL 

        if dept_time == "7:30 pm":
            time = Dept_Time.AT_730
        elif dept_time == "Alternate Time: Between 6 - 7:30 pm (You will be included in the 7:30 pickup lottery as well if you're a rider)":
            time = Dept_Time.BEFORE_730
        elif dept_time == "Alternate Time: After 7:30 pm":
            time = Dept_Time.AFTER_730
        
        # if member_type == "Driver":
            # Driver
        # elif member_type == "Rider":
            # Rider

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

def parse_dept_time(dept_time):
    """ Returns an enum for the departure times for tuesday and thursday. """
    if dept_time == "7:30 pm":
        return Dept_Time.AT_730
    elif dept_time == "Alternate Time: Between 6 - 7:30 pm (You will be included in the 7:30 pickup lottery as well if you're a rider)":
        return Dept_Time.BEFORE_730
    elif dept_time == "Alternate Time: After 7:30 pm":
        return Dept_Time.AFTER_730

def get_driver(array):
    """ Returns a Driver object. """
    #TODO FINISH THIS
    location = parse_location(array[1])
    dept_time = parse_dept_time(array[4])

