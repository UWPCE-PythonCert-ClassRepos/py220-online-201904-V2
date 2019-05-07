#!/usr/bin/env python3
# pylint: disable=E0401, C0111
"""This is lesson 02 activity redone in a more funcational sort of way"""

# Douglas Klos
# April 18th, 2019
# Python 220
# Lesson 04, Extra practice, functional programming

# So functional programming, I'm not sure if this is close or not.
# From what I can gather, you want to avoid unnecessary state changes.
# Functions should take in one piece of data, and return data that the next
# function can then consume.  Comprehensions instead of a for loop.  In the
# past it seems lambda, map, reduce, and filter were used a lot, but
# comprehensions appear to be more capable.  Also generators and iterators.
# Another method I tried of this used a generator and yield statment to
# serve up one row at a time.


import json
import math
from datetime import datetime
from loguru import logger


def calculate_additional_fields(data):
    try:
        data["total_days"] = (
            datetime.strptime(data["rental_end"], "%m/%d/%y") -
            datetime.strptime(data["rental_start"], "%m/%d/%y")
        ).days
        data["total_price"] = data["total_days"] * data["price_per_day"]
        data["sqrt_total_price"] = math.sqrt(data["total_price"])
        data["unit_cost"] = data["total_price"] / data["units_rented"]
    except (ZeroDivisionError, ValueError, KeyError) as ex:
        logger.debug(f"Value:{data}")
        logger.critical(ex)
    return data


def swap_dates(data):
    try:
        if datetime.strptime(
                data["rental_end"], "%m/%d/%y"
        ) < datetime.strptime(data["rental_start"], "%m/%d/%y"):
            logger.warning(f"Swapping dates")
            return {
                "product_code": data["product_code"],
                "units_rented": data["units_rented"],
                "price_per_day": data["price_per_day"],
                "rental_start": data["rental_end"],
                "rental_end": data["rental_start"],
            }
    except ValueError:
        logger.error(f"Value:{data} contains bad date data.  Skipping.")
    return data


def open_file(filename="./source.json"):
    return json.load(open(filename))


if __name__ == "__main__":
    json.dump(
        {
            key: calculate_additional_fields(swap_dates(value))
            for (key, value) in open_file().items()
        },
        open("./out.json", "w"),
    )
