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
# column_names = {'Timestamp': 'timestamp',
#                 'What version of python would you like to see used for the examples on the site?': 'version',
#                 'How useful is the content on practical business python?': 'useful',
#                 'What suggestions do you have for future content?': 'suggestions',
#                 'How frequently do you use the following tools? [Python]': 'freq-py',
#                 'How frequently do you use the following tools? [SQL]': 'freq-sql',
#                 'How frequently do you use the following tools? [R]': 'freq-r',
#                 'How frequently do you use the following tools? [Javascript]': 'freq-js',
#                 'How frequently do you use the following tools? [VBA]': 'freq-vba',
#                 'How frequently do you use the following tools? [Ruby]': 'freq-ruby',
#                 'Which OS do you use most frequently?': 'os',
#                 'Which python distribution do you primarily use?': 'distro',
#                 'How would you like to be notified about new articles on this site?': 'notify'
#                 }
# data.rename(columns=column_names, inplace=True)
# data.timestamp = pd.to_datetime(data.timestamp)
print(data.head())
