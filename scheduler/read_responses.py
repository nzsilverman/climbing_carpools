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
    # Put uniqnames of people who have paid dues into a list
    dues_list = set()
    for entry in dues_sheet:
        dues_list.add(entry["Uniqname"])

    return (data, dues_list)


def create_lists(sheet_name, dues_sheet_name):
    """ Parse data and return tuple in the form:
    (tues_drivers list, tues riders list, thurs drivers list, thurs riders list,
    sun drivers list, sun riders list) ."""
    
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
        

        # Create Tuesday Entry
        member_type = tues_array[0]
        if member_type == "Driver":
            # Driver Type
            driver = get_tues_thurs_driver(tues_array, email, name)
            validate_driver(tues_drivers, driver)
        elif member_type == "Rider":
            # Rider Type
            rider = get_tues_thurs_rider(tues_array, email, name)
            validate_rider(tues_riders, rider, dues_list)
        
        # Thursday array is entries [9, 15)
        thurs_array = row[9:15]

        # Create Thursday Entry
        member_type = thurs_array[0]
        if member_type == "Driver":
            # Driver Type
            driver = get_tues_thurs_driver(thurs_array, email, name)
            validate_driver(thurs_drivers, driver);
        elif member_type == "Rider":
            # Rider Type
            rider = get_tues_thurs_rider(thurs_array, email, name)
            validate_rider(thurs_riders, rider, dues_list)

        # Create sunday entry
        # Splice array from 15th element to the end
        sunday_array = row[15:] 

        member_type = sunday_array[0]
        if member_type == "Driver":
            # Driver Type
            driver = get_sunday_driver(sunday_array, email, name)
            validate_driver(sun_drivers, driver)
        elif member_type == "Rider":
            # Rider Type
            rider = get_sunday_rider(sunday_array, email, name)
            validate_rider(sun_riders, rider, dues_list)
    return (tues_drivers, tues_riders, thurs_drivers, thurs_riders, sun_drivers, sun_riders)

def validate_driver(array, driver):
    """ Validates driver has necesary info needed.
    Returns an array, either with the driver appended if valid
    or without the driver if not valid. """
    
    # Check to make sure dept_time is filled out, num riders filled out, and
    # location filled out
    if driver.dept_time and driver.num_riders and driver.loc:
        # Validate dept time is 730 or alt provided
        if driver.dept_time != Dept_Time.AT_730 and driver.dept_time != Dept_Time.AT_10_AM:
            # make sure alt provided
            if driver.alt_time:
                # Checks passed, append and return 
                array.append(driver)
        else:
            # Driver dept time is a standard time, add them
            array.append(driver)
    # else:
        # Checks failed, do not append
        # print("Validate driver failed for the following driver: " + driver.name)
        # print("Dept time: " + str(driver.dept_time))
        # print("Num Riders: " + str(driver.num_riders))
        # print("Loc: " + str(driver.loc))

def validate_rider(array, rider, dues_list):
    """ Validate a rider has necesary info, return array with rider if 
    valid and without rider if invalid. """
    # import pdb; pdb.set_trace()
    uniqname = rider.email.split('@')[0].strip()
    # Make sure there is a ride departure location and time
    if rider.loc and rider.dept_time:
        # Make sure they paid dues
        if uniqname in dues_list:
            array.append(rider)
        else:
            print("Validate rider failed for " + rider.name + ", " + uniqname + "@umich.edu" + " since they did not pay dues")
    # else:
        # If checks failed, list is unmodified
        # print("validate rider failed for the following rider: " + rider.name)

def parse_dept_time(dept_time):
    """ Returns an enum for the departure times for tuesday and thursday. """
    if dept_time == "7:30 pm":
        return Dept_Time.AT_730
    elif dept_time == "Alternate Time: Between 6 - 7:30 pm (You will be included in the 7:30 pickup lottery as well if you're a rider)":
        return Dept_Time.BEFORE_730
    elif dept_time == "Alternate Time: After 7:30 pm":
        return Dept_Time.AFTER_730

def parse_driver_location(dept_loc):
    """ Returns an enum for the location. """
    if dept_loc == "Exclusively departing from North campus":
        return Loc.NORTH 
    elif dept_loc == "Leaving from North and going to Central to pickup riders":
        return Loc.NORTH_AND_CENTRAL 
    elif dept_loc == "Exclusively departing from Central campus":
        return Loc.CENTRAL 

def parse_rider_location(dept_loc):
    """ Returns an enum for the location the rider will depart from. """
    if dept_loc == "Exclusively North campus":
        return Loc.NORTH 
    elif dept_loc == "Preferably North campus, but would go to Central if that was my only ride":
        return Loc.NORTH_AND_CENTRAL
    elif dept_loc == "Exclusively Central campus":
        return Loc.CENTRAL

def get_tues_thurs_driver(array, email, name):
    """ Returns a Driver object. """
    # Format of Data for Tuesday and Thursday
    # [0] type
    # [1] driver_departure
    # [2] driver_num_riders
    # [3] rider_departure
    # [4] departure_time
    # [5] alt_time

    location = parse_driver_location(array[1])
    if array[2]:
        num_riders = int(array[2])
    else:
        num_riders = 0
    dept_time = parse_dept_time(array[4])
    alt_time = array[5]

    return Driver(email, name, location, num_riders, dept_time, alt_time)

def get_tues_thurs_rider(array, email, name):
    """ Returns a Rider object. """
    # Format of Data for Tuesday and Thursday
    # [0] type
    # [1] driver_departure
    # [2] driver_num_riders
    # [3] rider_departure
    # [4] departure_time
    # [5] alt_time

    location = parse_rider_location(array[3])
    dept_time = parse_dept_time(array[4])

    return Rider(email, name, location, dept_time) 

def get_sunday_driver(array, email, name):
    # Array has the form
    # [0] type
    # [1] driver departure
    # [2] driver num riders
    # [3] rider departure
    location = parse_driver_location(array[1])
    if array[2]:
        num_riders = int(array[2])
    else:
        num_riders = 0
    dept_time= Dept_Time.AT_10_AM

    # Return a Driver for 10 am, no alternate time
    return Driver(email, name, location, num_riders, dept_time, 0)  

def get_sunday_rider(array, email, name):
    # Array has the form
    # [0] type
    # [1] driver departure
    # [2] driver num riders
    # [3] rider departure
    location = parse_rider_location(array[3])
    dept_time = Dept_Time.AT_10_AM

    # Return a Rider for 10 am, no alternate time
    return Rider(email, name, location, dept_time)  
