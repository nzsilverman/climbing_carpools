from scheduler.classes.Member import Member


class Driver(Member):
    """Driver class for representing a climbing club member that has a car
    and offers rides to members without cars

    Subclass of a member

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
        car_type:
            string of a short description of this driver's car
        seats:
            number of seats available for riders
        seats_remaining:
            number of seats remaining in the car. Initialized to same number as seats param

    Typical Usage:
        member = Driver("John Foo", "foo@bar.com", "9876543211", [DayInfo(DayName.MONDAY, [6], ["NORTH", "CENTRAL"])], false, "red toyota", 4)
    """

    def __init__(self, name: str, email: str, phone: str, days: list,
                 is_dues_paying: bool, car_type: str, seats: int):
        super().__init__(name, email, phone, days, is_dues_paying)
        self.car_type: str = car_type
        self.seats: int = seats
        self.seats_remaining: int = seats
