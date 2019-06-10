import csv


def add_furniture(invoice_file, customer_name, item_code,
                  item_description, item_monthly_price):
    with open(invoice_file, 'a',  newline='') as file:
        writer = csv.writer(file)
        data = customer_name, item_code, item_description, item_monthly_price
        writer.writerow(data)
    return customer_name, item_code, item_description, item_monthly_price


def single_customer(customer_name, invoice_file):
    def single_closure(input_file):
        with open(input_file, 'r') as file:
            data = []
            for lines in file:
                lines = lines.strip().split(',')
                data.append([lines[0], lines[1], float(lines[2])])
        for lines in data:
            add_furniture(invoice_file, customer_name,
                          lines[0], lines[1], lines[2])
        return data
    return single_closure


if __name__ == "__main__":
    add_furniture("rented_items.csv", "Elisa Miles",
                  "LR04", "Leather Sofa", 25.00)
    add_furniture("rented_items.csv", "Edward Data",
                  "KT78", "Kitchen Table", 10.00)
    add_furniture("rented_items.csv", "Alex Gonzales",
                  "BR02", "Queen Mattress", 17.00)
    CREATE_INVOICE = single_customer("Susan Wong", "rented_items.csv")
    CREATE_INVOICE("test_items.csv")