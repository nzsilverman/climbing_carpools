from oauth2client.service_account import ServiceAccountCredentials
import gspread


class AuthorizedClient:
    _instance = None

    @staticmethod
    def _authorize() -> None:
        """
        Authorizes this client
        """

        SCOPE = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive",
        ]
        SECRETS_FILE = "secret.json"

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            SECRETS_FILE, SCOPE)

        return gspread.authorize(credentials), credentials

    def __init__(self):
        if AuthorizedClient._instance is not None:
            raise Exception("Authorized client error")
        else:
            self.client, self.credentials = AuthorizedClient._authorize()
            AuthorizedClient._instance = self

    @classmethod
    def get_instance(cls):
        """
        Get instance of this client
        """

        if cls._instance is None:
            cls()
        return cls._instance
