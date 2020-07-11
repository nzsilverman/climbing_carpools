from scheduler.classes.Member import Member

class Driver(Member):
    
    def __init__(self, name, email, phone, days, car_type, seats):
        super().__init__(name, email, phone, days)
        self.car_type = car_type
        self.seats = seats

        