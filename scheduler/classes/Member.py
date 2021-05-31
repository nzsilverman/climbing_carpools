import scheduler.classes.Day as Day


class Member:
    """Member class for representing a climbing club member

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
        member = Member("John Foo", "foo@bar.com", "9876543211", [DayInfo(DayName.MONDAY, [6, 7, 8], ["NORTH", "CENTRAL"])], false)
    """

    # TODO: phone number str or int? I'm thinking str
    def __init__(self, name: str, email: str, phone: str, days: list,
                 is_dues_paying: bool):
        self.name: str = name
        self.email: str = email
        self.phone: str = phone
        self.days: list = days
        self.is_dues_paying: bool = is_dues_paying

    def get_locations(self, day: Day.DayName) -> list():
        for d in self.days:
            if d.day == day:
                return d.locations

        return list()

    def get_times(self, day: Day.DayName) -> list():
        for d in self.days:
            if d.day == day:
                return d.times

        return list()
