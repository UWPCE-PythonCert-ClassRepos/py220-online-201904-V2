'''
1. You will create a program to initially create, and subsequently update,
a CSV file that lists which furniture is rented to which customer (to replace
use of the spreadsheet mentioned above).
2. You will create additionally functionality that will load individual
customers rentals.
'''
#from functools import partial

def add_furniture(invoice_file, customer_name, item_code,
                  item_description, item_monthly_price):
    '''add customer data to a csv file'''
    with open(invoice_file, 'a', encoding='utf-8-sig') as file:
        file.write('{:},{:},{:},{:.2f}\n'.format(customer_name,
                                                 item_code,
                                                 item_description,
                                                 item_monthly_price))
    return (invoice_file, customer_name, item_code,
            item_description, item_monthly_price)

def single_customer(customer_name, invoice_file):
    '''add items to a source file with a fixed customer name
    and destination inventory file'''
    def single_closure(input_file):
        with open(input_file, 'r') as file:
            data = []
            for line in file:
                line = line.strip().split(',')
                data.append([line[0], line[1], float(line[2])])
        for line in data:
            add_furniture(invoice_file, customer_name,
                          line[0], line[1], line[2])
        return data
    return single_closure


if __name__ == "__main__":
    PATH = "../data/"
    add_furniture(PATH + "rented_items.csv", "Elisa Miles",
                  "LR04", "Leather Sofa", 25)
    add_furniture(PATH + "rented_items.csv", "Edward Data",
                  "KT78", "Kitchen Table", 10)
    add_furniture(PATH + "rented_items.csv", "Alex Gonzales",
                  "BR02", "Queen Mattress", 17)
    CREATE_INVOICE = single_customer("Susan Wong", PATH + "rented_items.csv")
    CREATE_INVOICE(PATH + "test_items.csv")
