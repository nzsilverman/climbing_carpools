from oauth2client.service_account import ServiceAccountCredentials
import gspread


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

    # TODO -> I am a little confused why we need to keep track of this. It seems a little convoluted
    # and might be better served reworking how we interact with this class to obtain an authorized client
    # the decorators for staticmethod and classmethod should go in accordance with the Google style guide
    _instance = None

    # TODO don't use static methods and limit use of classmethods (i.e we can prob get rid of em). Google style guide says this
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
