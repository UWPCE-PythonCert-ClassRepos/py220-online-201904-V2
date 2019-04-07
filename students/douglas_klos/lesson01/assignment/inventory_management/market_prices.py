"""A useless module intended to mock us (for us to mock)

The assignment had contradictory instructions:
  It stated to ensure pylint ./inventory_management/ had a score of 10.
  It also stated not to alter this file.
  This file needed altering to score 10 on pylint,
  but I left it as a broken function so that mock is still required.

"""


def get_latest_price(item_code):
    """Gets latest market price for item code

    Args:
        item_code (int) : item to get price for

    Returns:
        Should return the market price for specified item.
        Instead it returns only the argument item_code

    """
    return item_code
    # return 24
    # Raise an exception to force the user to Mock its output
