""" import partial as factory function """
import os
from functools import partial


def add_furniture(invoice_file, customer_name, item_code, item_description, item_monthly_price):
    """ add items to invoice file with input parameters """
    if os.path.isfile(invoice_file):
        open_mode = 'a'
    else:
        open_mode = 'w'
    with open(invoice_file, open_mode) as fout:
        fout.write('%s,%s,%s,%s\n' % (customer_name, item_code,
                                      item_description, item_monthly_price))


def single_customer(customer_name, invoice_file):
    """ functools and closures to add rental items """

    add_customer_rental = partial(add_furniture, invoice_file, customer_name)

    def add_rental_items(rental_items):
        with open(rental_items, 'r') as fin:
            for line in fin.readlines():
                [item_code, item_description, item_monthly_price] = line.rstrip(
                    '\n').split(',')
                add_customer_rental(
                    item_code, item_description, item_monthly_price)

    return add_rental_items


def main():
    """ runs program as main """

    add_furniture("rented_items.csv", "Elisa Miles",
                  "LR04", "Leather Sofa", 25)
    add_furniture("rented_items.csv", "Edward Data",
                  "KT78", "Kitchen Table", 10)
    add_furniture("rented_items.csv", "Alex Gonzales",
                  "BR02", "Queen Mattress", 17)

    create_invoice = single_customer("Susan Wong", "rented_items.csv")
    create_invoice("../data/test_items.csv")


if __name__ == '__main__':
    main()
