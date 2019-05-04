#!/usr/bin/env python

"""
demo OO vs FP
"""

class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
 
    def change_salary(self, amt):
       self.salary = self.salary + amt
 
    def describe(self):
       print(f"oo {self.name} makes {self.salary}")


def oo(employees):
    for employee in employees:
        happier_employee = Employee(employee[0], employee[1])
        happier_employee.change_salary(200)
        happier_employee.describe()


# def fp1(employees):
def fp1(employees, adjustment):    
    happier_employees = []
    for employee in employees:
        # happier_employees.append((employee[0], employee[1] + 200))
        happier_employees.append((employee[0], adjustment(employee[1], 200)))
    return happier_employees


def fp2(employees):
    for employee in employees:
        print(f"fp {employee[0]} makes {employee[1]}")


def adjust(value, by):
    return value + by

if __name__ == "__main__":
    
    emps = [
        ("andy", 34000),
        ("fred", 75000),
    ]

    oo(emps)

    # happies = fp1(emps)
    happies = fp1(emps, adjust)
    fp2(happies)