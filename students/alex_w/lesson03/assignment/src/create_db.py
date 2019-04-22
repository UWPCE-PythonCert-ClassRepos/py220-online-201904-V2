import sys
import logging
import time
import argparse
import db_models 
from peewee import IntegrityError



logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)


def main():
    """Initializes customer database
    """
            
    start = time.time()
    args = parse_cmd_arguments()
    LOGGER.info("Initializes the HP Norton database from csv")
    LOGGER.info("Adding tables...")
    add_tables()
    if not args.blank:
        populate_database(args.input)
    LOGGER.info("Closing database")
    db_models.database.close()
    LOGGER.info("Time to init: %s", time.time() - start)    



def parse_cmd_arguments():
    """Parses the command line arguments. """
    
    parser = argparse.ArgumentParser(description="Build customer database")
    parser.add_argument("-i", "--input", help="input CSV file", required=True)
    parser.add_argument(
        "-b",
        "--blank",
        help="column headers only, no row data",
        action="store_true",
        required=False,
        default=False,
    )
    parser.add_argument("-d", "--debug", help="debugger level", required=False)

    return parser.parse_args()



def add_tables():
    """Adds tables to database"""
    db_models.database.create_tables([db_models.Customer])



def populate_database(filename):
    """Populates database from csv file."""
    
    with open(filename, "rb") as cvs_file:
        next(cvs_file)  # Skip first line, it's the column names
        lines = cvs_file.read().decode("utf-8", errors="ignore").split("\n")
        for line in lines:
            customer = line.split(",")
            try:
                with db_models.database.transaction():
                    db_models.Customer.create(
                        customer_id=customer[0],
                        name=customer[1],
                        last_name=customer[2],
                        home_address=customer[3],
                        phone_number=customer[4],
                        email_address=customer[5],
                        status=customer[6].lower(),
                        credit_limit=customer[7],
                    )
                    LOGGER.info("Adding record for %s", customer[0])
            except IndexError:
                LOGGER.info("End of file")
            except IntegrityError:
                LOGGER.info("Records already in database. Exiting.")
                sys.exit(0)




if __name__ == "__main__":
    main()
    