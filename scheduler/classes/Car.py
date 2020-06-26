class Car:
    """
    Car.
    """

    def __init__(self, driver):
        self.driver = driver
        self.seats = driver["seats"]
        self.riders = []
