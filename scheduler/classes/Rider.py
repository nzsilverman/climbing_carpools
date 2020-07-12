from scheduler.classes.Member import Member


class Rider(Member):
    """Rider represents a Member that does not drive and needs to be matched with a Driver
    Used to improve readability

    Attributes:
        name:
            string of member name
        email:
            string of member email
        phone:
            string of member phone number
        days:
            list of DayInfo objects representing the days this member
            participating in the carpools
        is_dues_paying:
            boolean value, true if this member has paid club membership dues, false otherwise

    Typical Usage:
        member = Rider("John Foo", "foo@bar.com", "9876543211", [DayInfo(DayName.MONDAY, [6, 7, 8], ["NORTH", "CENTRAL"])], false)
    """

    def __init__(self, name: str, email: str, phone: str, days: list, is_dues_paying: bool):
        super().__init__(name, email, phone, days, is_dues_paying)
