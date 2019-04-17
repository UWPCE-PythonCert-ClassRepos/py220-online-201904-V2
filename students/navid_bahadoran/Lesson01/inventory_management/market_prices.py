"""return the latest price"""


def get_latest_price(item_code=None):
    """

    :param item_code: item code in the inventory
    :return: return the latest price
    """
    if item_code:
        return 24
    return None
    # Raise an exception to force the user to Mock its output
