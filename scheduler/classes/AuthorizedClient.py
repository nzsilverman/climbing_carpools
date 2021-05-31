import gspread
from oauth2client.service_account import ServiceAccountCredentials


class AuthorizedClient:
    """Get an authorized client able to read/ write to google drive.

    Uses the secret.json file that an operator of the program is expected to have

    Attributes:
        client:
            Authorized client that can interact with google drive
        credentials:
            credentials of the authorized client
        _instance:
            assigned to 'self' attribute of the class

    Typical Usage:
        import AuthorizedClient
        client = AuthorizedClient.get_instance().client
    """

    _instance = None

    def _authorize(self) -> (gspread.client.Client, ServiceAccountCredentials):
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
            self.client, self.credentials = AuthorizedClient._authorize(self)
            AuthorizedClient._instance = self

    @classmethod
    def get_instance(cls):
        """
        Get instance of this client
        """

        if cls._instance is None:
            cls()
        return cls._instance
