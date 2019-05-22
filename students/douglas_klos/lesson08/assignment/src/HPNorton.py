#!/usr/bin/env python3

from inventory import inventory

def main():

    func = inventory.single_customer_search('Douglas Klos', '../data/invoice.csv')
    print(func('FG00'))
    print(func('FG204'))

    func = inventory.single_customer('Hououin Kyouma', '../data/invoice.csv')
    func('../data/items.csv')


if __name__ == "__main__":
    main()
