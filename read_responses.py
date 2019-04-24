from __future__ import print_function
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
SECRETS_FILE = "secret.json"
SPREADSHEET = "Carpool Scheduling Template (Responses)"
# Based on docs here - http://gspread.readthedocs.org/en/latest/oauth2.html
# Load in the secret JSON key (must be a service account)
json_key = json.load(open(SECRETS_FILE))
# Authenticate using the signed key
# credentials = SignedJwtAssertionCredentials(json_key['client_email'],
#                                             json_key['private_key'], SCOPE)
credentials = ServiceAccountCredentials.from_json_keyfile_name('secret.json', SCOPE)

gc = gspread.authorize(credentials)
print("The following sheets are available")
for sheet in gc.openall():
    print("{} - {}".format(sheet.title, sheet.id))
# Open up the workbook based on the spreadsheet name
workbook = gc.open(SPREADSHEET)
# Get the first sheet
sheet = workbook.sheet1
# Extract all data into a dataframe
data = pd.DataFrame(sheet.get_all_records())
# Do some minor cleanups on the data
# Rename the columns to make it easier to manipulate
# The data comes in through a dictionary so we can not assume order stays the
# same so must name each column
column_names = {'Timestamp': 'timestamp',
                'Email Address': 'email',
                'Are you a driver or a rider?': 't_type',
                'DRIVER ONLY: Where will you be departing/ picking up?': 't_driver_departure',
                'DRIVER ONLY: How many riders can you take?': 't_driver_num_riders',
                'RIDER ONLY: Where will you be departing from?': 't_rider_departure',
                'What time will you be departing? ': 't_departure_time',
                'If you are a driver and entered an alternate time, please enter the exact time you will be departing': 't_alt_time',
                'Are you a driver or a rider?' : 'th_type',
                'DRIVER ONLY: Where will you be departing/ picking up?' : 'th_driver_departure',
                'DRIVER ONLY: How many riders can you take? ': 'th_driver_num_riders',
                'RIDER ONLY: Where will you be departing from?' : 'th_rider_departure',
                'What time will you be departing? ':'th_departure_time',
                'If you are a driver and entered an alternate time, please enter the exact time you will be departing': 'th_alt_time',
                'Are you a driver or a rider?': 's_type',
                'DRIVER ONLY: Where will you be departing/ picking up?': 's_driver_departure',
                'DRIVER ONLY: How many riders can you take? ': 's_driver_num_riders',
                'RIDER ONLY: Where will you be departing from?' : 's_rider_departure'
                }
data.rename(columns=column_names, inplace=True)
data.timestamp = pd.to_datetime(data.timestamp)
print(data.head())
