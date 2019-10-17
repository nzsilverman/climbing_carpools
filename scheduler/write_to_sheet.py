""" write_to_sheet.py 
    This module is for writing the output to a google sheet. """

from classes.Loc import Loc
from classes.Dept_Time import Dept_Time
from classes.Driver import Driver
from classes.Rider import Rider
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import time

def populate_values_array(matched_dict, values):
    for driver in matched_dict:
        array = ["Driver Name:", str(driver.name), "Phone: ", str(driver.phone), "Loc: ", str(driver.loc), "Empty Seats: ", int(matched_dict[driver]["seats_left"]), "Time: ", str(driver.dept_time), "Alt time (if not 7:30): ", str(driver.alt_time)]
        values.append(array)
        for rider in matched_dict[driver]["riders"]:
            array = ["Rider Name:", str(rider.name), "Phone: ", str(rider.phone)] 
            values.append(array)

        # Append empty to write an empty row in between drivers
        values.append([])

def write_to_gsheet(matched_tues, matched_thurs, matched_sun, spreadsheet_name):
    """ print the matched dict with all info, for the debug. It has the format:
    {Driver: {'seats_left': #, 'riders': [Rider, ..., Rider]}, ...} """
    
    SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    SECRETS_FILE = "secret.json" 
    # Load in the secret JSON key (must be a service account)
    json_key = json.load(open(SECRETS_FILE))
    # Authenticate using the signed key
    credentials = ServiceAccountCredentials.from_json_keyfile_name('secret.json', SCOPE)
    gc = gspread.authorize(credentials)

    # Open up the workbook based on the spreadsheet name
    spreadsheet = gc.open(spreadsheet_name)

    # Get the first sheet
    sheet = spreadsheet.sheet1

    values_tues = []
    populate_values_array(matched_tues, values_tues)

    values_thurs = []
    populate_values_array(matched_thurs, values_thurs)

    values_sun = []
    populate_values_array(matched_sun, values_sun)

    # index starts at 1
    index = 1

    row = ["Tuesday Rides"]
    sheet.insert_row(row, index)
    index += 1

    # Loop through all tuesday values
    for row in values_tues:
        sheet.insert_row(row, index)
        time.sleep(.3)
        index += 1

    row = ["Thursday Rides"]
    sheet.insert_row(row, index)
    time.sleep(.3)
    index += 1

    # Loop through all thursday values
    for row in values_thurs:
        sheet.insert_row(row, index)
        time.sleep(.3)
        index += 1

    row = ["Sunday Rides"]
    sheet.insert_row(row, index)
    time.sleep(.3)
    index += 1

    # Loop through all sunday values
    for row in values_sun:
        sheet.insert_row(row, index)
        time.sleep(.3)
        index += 1
