class Locke:
    def __init__(self, locke_capacity):
        print("locke init")
        self.locke_capacity = locke_capacity
        self.starting_pumps = "Starting the pumps"
        self.stopping_pumps = "Stopping the pumps"
        self.open_doors = "Opening the doors"
        self.close_doors = "Closing the doors"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("locke exit")

    def move_boats_through(self, boats):
        """
        Moves boats through the locke based on the lockes capacity defined at
        initialization.
        """
        if boats > self.locke_capacity:
            raise ValueError("Too many boats for this size locke!!")
            # print("Too many boats for this size locke!")
        else:
            print(self.stopping_pumps)
            print(self.open_doors)
            print(self.close_doors)
            print(self.starting_pumps)


if __name__ == '__main__':
    small_locke = Locke(5)
    large_locke = Locke(10)

    with large_locke as locke:
        locke.move_boats_through(8)

    with small_locke as locke:
        locke.move_boats_through(8)
    
