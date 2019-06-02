import logging

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
CONSOLE = logging.StreamHandler()
CONSOLE.setFormatter(FORMATTER)
CONSOLE.setLevel(logging.INFO)
LOGGER.addHandler(CONSOLE)


class LockOverload(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message

    pass


class Locke:
    def __init__(self, capacity):
        self.__capacity = capacity

    def __enter__(self):
        LOGGER.info("Try to Open the Lock")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        LOGGER.info("Locks are going to be closed")
        self.stop_pumps()
        self.open_upstream_door()
        self.close_upstream_door()
        self.open_downstream_door()
        self.close_downstream_door()
        self.start_pumps()

    @staticmethod
    def stop_pumps():
        LOGGER.info("Stopping the pumps.")

    @staticmethod
    def start_pumps():
        LOGGER.info("Restarting the pumps.")

    @staticmethod
    def open_upstream_door():
        LOGGER.info("Opening the upstream doors.")

    @staticmethod
    def close_upstream_door():
        LOGGER.info("Closing the upstream doors.")

    @staticmethod
    def open_downstream_door():
        LOGGER.info("Opening the downstream doors.")

    @staticmethod
    def close_downstream_door():
        LOGGER.info("Closing the downstream doors.")

    def move_boats_through(self, boats_count):
        try:
            if boats_count > self.__capacity:
                raise LockOverload("Locks are overloaded, Boats cannot pass!!")
            self.stop_pumps()
            self.open_upstream_door()
            self.close_upstream_door()
            self.open_downstream_door()
            self.close_downstream_door()
            self.start_pumps()
        except LockOverload as e:
            LOGGER.warning(e)


if __name__ == '__main__':
    small_locke = Locke(5)
    large_locke = Locke(10)
    boats = 8
    # Too many boats through a small locke will raise an exception
    with small_locke as locke:
        locke.move_boats_through(boats)

    # A lock with sufficient capacity can move boats without incident.
    with large_locke:
        large_locke.move_boats_through(boats)
