from __future__ import print_function
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

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
cols = ['timestamp', 'email', 't_type', 't_driver_departure', 't_driver_num_riders', 't_rider_departure', \
        't_departure_time', 't_alt_time', 'th_type', 'th_driver_departure', 'th_driver_num_riders', \
        'th_rider_departure', 'th_departure_time', 'th_alt_time', 's_type', 's_driver_departure', \
        's_driver_num_riders', 's_rider_departure']
# data = sheet.get_all_records()
data = sheet.get_all_values() # Reads in as a list of lists, doesn't combine dict entries

for item in data:
    print(item)
    print('Len: {}'.format(len(item)))
    print('\n')

# Get due paying members list
dues_sheet = gc.open(DUES_SHEET).sheet1.get_all_records()
# uniquenames of people who have paid dues
dues_list = []
for entry in dues_sheet:
    dues_list.append(entry["Uniquename"])
print(dues_list)


# key = email address
row_dict = {}
