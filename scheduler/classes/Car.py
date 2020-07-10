class Car:
    """
    Car
    """

    def __init__(self, driver: dict):
        self.driver = driver
        self.car_type: str = driver["car_type"]
        self.seats: int = driver["seats"]
        self.riders = list()
    # def __init__(self, driver: dict):
    #     self.driver: dict = driver
    #     self.car_type: str = driver["car_type"]
    #     self.seats: int = driver["seats"]
    #     self.riders = list()
