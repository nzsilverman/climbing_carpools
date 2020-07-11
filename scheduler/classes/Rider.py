from scheduler.classes.Member import Member

class Rider(Member):

    def __init__(self, name, email, phone, days, is_dues_paying):
        super().__init__(name, email, phone, days)
        self.is_dues_paying = is_dues_paying
