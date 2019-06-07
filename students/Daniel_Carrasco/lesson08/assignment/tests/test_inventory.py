"""
    Autograde Lesson 8 assignment

"""

import inventory as l


def test_add_furniture():
    """
    test for add furniture, that creates csv
    """
    l.add_furniture(
        "test_invoice_file.csv",
        "Elisa Miles",
        "LR04",
        "Leather Sofa",
        "25.00")
    test_last = open("test_invoice_file.csv", "r")
    last_line = test_last.readlines()[-1].strip('\n')
    input_line = 'Elisa Miles,LR04,Leather Sofa,25.00'
    assert last_line == input_line
    l.add_furniture(
        "test_invoice_file.csv",
        "Edward Data",
        "KT78",
        "Kitchen Table",
        "10.00")
    last_line = test_last.readlines()[-1].strip('\n')
    second_input = 'Edward Data,KT78,Kitchen Table,10.00'
    assert last_line == second_input
    test_last.close()


def test_single_customer():
    """
    test for single customer function that uses partial
    """
    a_test = l.single_customer("test_invoice_file.csv", "Susan Wong")
    b_test = a_test("test_items.csv")
    assert b_test[0] == ('Susan Wong', 'LR01', 'Small lamp', '7.50')
