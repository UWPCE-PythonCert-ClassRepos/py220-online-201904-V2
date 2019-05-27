"""Functional Method"""


import csv


def add_furniture(invoice_file="", customer_name="", item_code="",
                  item_description="", item_monthly_price=""):

    """
   add to or creates invoice file, add customer data
    """
    with open(invoice_file, "a+", newline='') as csvfile:
        writer = csv.writer(csvfile)
        row = customer_name, item_code, item_description, item_monthly_price
        writer.writerow(row)
    return(invoice_file, customer_name, item_code,
           item_description, item_monthly_price)


def single_customer(customer_name, invoice_file):
    """Closure for a single customer and file"""
    def add_rentals(rental_file):
        """add rental info for individual
           customer
        """
        with open(rental_file, 'r') as rental_csv:
            customer_data = []
            for row in rental_csv:
                row = row.strip().split(',')
                customer_data.append([row[0], row[1], float(row[2])])
        for row in customer_data:
            add_furniture(invoice_file, customer_name,

                          row[0], row[1], row[2])
        return customer_data
    return add_rentals



if __name__ == "__main__":

    add_furniture("../data/invoice_file.csv", "Elisa Miles", "LR04", "Leather Sofa", "25.00")
    add_furniture("../data/invoice_file.csv", "Edward Data", "KT78", "Kitchen Table", "10.00")
    add_furniture("../data/invoice_file.csv", "Alex Gonzales", "BR02", "Queen Matress", "17.00")
    CREATE_INVOICE = single_customer("Susan Wong", "../data/invoice_file.csv")
    CREATE_INVOICE("../data/test_items.csv")
