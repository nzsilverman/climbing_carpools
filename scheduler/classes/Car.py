from scheduler.classes.Driver import Driver


class Car:
    """Car class for representing the data needed for a car
    
    Attributes:
        driver:
            Driver object
        car_type:
            string of the cars type
        seats:
            integer of the number of seats in the car
        riders:
            list of the riders in the car

    Typical Usage:
        car = Car(driver)
    """

    def __init__(self, driver: Driver):
        self.driver: dict = driver
        self.car_type: str = driver.car_type
        self.seats: int = driver.seats
        self.riders = list()
