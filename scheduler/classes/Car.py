class Car:
    """
    Car
    """

    def __init__(self, driver):
        self.driver = driver
        self.car_type = driver["car_type"]
        self.seats = driver["seats"]
        self.riders = []
