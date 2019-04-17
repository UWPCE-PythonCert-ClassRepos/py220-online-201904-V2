#!/usr/bin/env python3

from database import db_model
from datetime import datetime

PEOPLE = "people"
JOB = "job"
DEPARTMENT = "department"


def main():
    dbms = db_model.MyDatabase(db_model.SQLITE, dbname='mydb.sqlite')
    dbms.create_db_tables()
    dbms.print_all_data(db_model.PEOPLE)
    dbms.print_all_data(db_model.JOB)
    dbms.insert_people()
    dbms.insert_departments()
    dbms.insert_jobs()
        
    query = f"SELECT * FROM {JOB}"
    result = dbms.query_db(query)
    for item in result:
        try:
            start_date = datetime.strptime(item[1], "%Y-%m-%d")
            end_date = datetime.strptime(item[2], "%Y-%m-%d")
            days_held = (end_date - start_date).days
            print(f"Job {item[0]} was held for {days_held} days")
        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    main()
