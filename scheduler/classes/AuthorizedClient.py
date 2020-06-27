from oauth2client.service_account import ServiceAccountCredentials
import gspread

class AuthorizedClient:
    __instance = None

    @staticmethod
    def __authorize():
        SCOPE = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        SECRETS_FILE = "secret.json"

        # json_key = json.load(open(SECRETS_FILE))

        credentials = ServiceAccountCredentials.from_json_keyfile_name(SECRETS_FILE, SCOPE)

        return gspread.authorize(credentials)
    
    def __init__(self):
        if AuthorizedClient.__instance != None:
            raise Exception("Singleton error")
        else:
            self.client = AuthorizedClient.__authorize()
            AuthorizedClient.__instance = self

    @staticmethod
    def get_instance():
        if AuthorizedClient.__instance == None:
            AuthorizedClient()
        return AuthorizedClient.__instance

