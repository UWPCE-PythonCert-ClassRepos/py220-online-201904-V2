""" Timer Logger class / metaclass / function definitions """
#pylint: disable=W0613, E1120
from types import MethodType, FunctionType
from datetime import datetime
from time import perf_counter
from wrapt import decorator


class TimerLogger():
    """ Generic context manager to time and log function / method calls """

    def __init__(self, function, *args, logfile="timings.txt", **kwargs):
        self._elapsed = 0.0
        self._start = None
        self._start_time = None

        self._function = function
        self._args = list(filter(lambda x: x != logfile, args))
        self._logilfe = logfile
        self._kwargs = kwargs

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, *args):
        self.stop()

    def start(self):
        """ Begin timing of method """

        self._start = perf_counter()
        self._start_time = datetime.now()

    def stop(self):
        """ End timing, calculate results, and write to self._logfile """

        end = perf_counter()
        self._elapsed = end - self._start

        with open(self._logilfe, "a") as log_file:
            log_file.write(
                f"{self._function.__name__} "
                f"called at {self._start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"\targs:{self._args}, kwargs:{self._kwargs}\n"
                f"\tFunction/Method execution time {self._elapsed} seconds\n"
            )


class HPNortonTimerLogger(TimerLogger):
    """ Overloading default TimerLogger stop() method """

    def stop(self):
        """ Overloads TimerLogger.stop() method to include record count """

        end = perf_counter()
        self._elapsed = end - self._start

        with open(self._logilfe, "a") as log_file:
            log_file.write(
                f"{self._function.__name__} "
                f"called at {self._start_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            )
            if (
                    self._function.__name__ == "insert_to_mongo" or
                    self._function.__name__ == "get_line_from_file"
            ):
                record_count = 0
                for _ in open(self._args[0]):
                    record_count += 1
                log_file.write(f"\tCalled on {record_count} records\n")
            else:
                log_file.write(f"\targs:{self._args}, kwargs:{self._kwargs}\n")
            log_file.write(
                f"\tFunction/Method execution time {self._elapsed} seconds\n"
            )


class TimedLogged(type):
    """ Metaclass to wrap children with timer_logger_func """

    def __new__(cls, name, bases, attr):
        for key, value in attr.items():
            if isinstance(value, (FunctionType, MethodType)):
                attr[key] = timer_logger_func(value)

        return super(TimedLogged, cls).__new__(cls, name, bases, attr)


@decorator
def timer_logger_func(function, instance, args, kwargs):
    """ Method / Function wrapper to time and log calls """

    with HPNortonTimerLogger(function, *args, "timings.txt", **kwargs):
        result = function(*args, **kwargs)
    return result
