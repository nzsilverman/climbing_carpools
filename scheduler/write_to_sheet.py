""" write_to_sheet.py 
    This module is for writing the output to a google sheet. """

from classes.Loc import Loc
from classes.Dept_Time import Dept_Time
from classes.Driver import Driver
from classes.Rider import Rider
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

def write_to_gsheet(matched_dict, spreadsheet_name):
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

    values = []
    for driver in matched_dict:
        array = ["Driver Name:", str(driver.name), "Phone: ", str(driver.phone), "Loc: ", str(driver.loc), "Empty Seats: ", int(matched_dict[driver]["seats_left"])]
        values.append(array)
        for rider in matched_dict[driver]["riders"]:
            array = ["Rider Name:", str(rider.name), "Phone: ", str(rider.phone)] 
            values.append(array)

    index = 1
    for row in values:
        sheet.insert_row(row, index)
        index += 1
