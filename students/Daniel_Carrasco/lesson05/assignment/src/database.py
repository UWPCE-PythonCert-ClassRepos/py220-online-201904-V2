LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
FORMATTER = logging.Formatter(LOG_FORMAT)

FILE_HANDLER = logging.FileHandler('db.log')
FILE_HANDLER.setLevel(logging.INFO)
FILE_HANDLER.setFormatter(FORMATTER)

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
LOGGER.addHandler(FILE_HANDLER)


class MongoDBConnection():
    """
    Class to start MongoDB Connection
    """

    def __init__(self, host='127.0.0.1', port=27017):
        """ be sure to use the ip address not name for local windows"""
        self.host = host
        self.port = port
        self.connection = None

    def __enter__(self):
        self.connection = MongoClient(self.host, self.port)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()


def import_data(directory_name, product_file, customer_file, rentals_file):
    """
    method to import the csv files that will be added to the db
    """
    LOGGER.info("starting MongoDBConnection")
    mongo = MongoDBConnection()

    with mongo:

        # mongodb database; it all starts here
        db = mongo.connection.HPNorton

        # collection in database
        products = db["products"]
        customers = db["customers"]
        rentals = db["rentals"]
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()

        LOGGER.info("importing data")
        product_ip = read_data(directory_name, product_file)
        customer_ip = read_data(directory_name, customer_file)
        rentals_ip = read_data(directory_name, rentals_file)

        product_results = add_many_ip(products, product_ip)
        customer_results = add_many_ip(customers, customer_ip)
        rental_results = add_many_ip(rentals, rentals_ip)

    import_count = (
        db.products.count_documents({}),
        db.customers.count_documents({}),
        db.rentals.count_documents({})
    )

    LOGGER.info(f'succesful product imports = {import_count[0]} to db')
    LOGGER.info(f'succesful customer imports = {import_count[1]} to db')
    LOGGER.info(f'succesful rental imports = {import_count[2]} to db')

    error_count = (product_results, customer_results, rental_results)
    LOGGER.info(f'product import errors = {error_count[0]} to db')
    LOGGER.info(f'customer import errors = {error_count[1]} to db')
    LOGGER.info(f'rental import errors = {error_count[2]} to db')

    return import_count, error_count


def read_data(directory_name, file_name):
    """
    method to read in the csv files
    """
    LOGGER.info(f'reading {file_name} data from {directory_name}')
    ip_list = []

    try:
        with open(directory_name + file_name) as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader, None)
            header[0] = header[0].replace("\ufeff", "")

            for row in reader:
                temp_dict = {}
                for index, value in enumerate(header):
                    temp_dict[value] = row[index]
                ip_list.append(temp_dict)
        LOGGER.info("successfully read in data")

    except Exception as error:
        LOGGER.info(f'could not read data due to {error}')

    return ip_list


def add_many_ip(collection_name, collection_ip):
    """
    method to add the data to the collection
    """

    try:
        collection_name.insert_many(collection_ip)
        LOGGER.info(f'no errors importing to {collection_name} ')
        error = 0
        return error
    except Exception as error:
        LOGGER.info(f'add_many_ip error of {error} for to {collection_name}')
        error = 1
        return error


def show_available_products():
    """
    Method to show available products
    """
    mongo = MongoDBConnection()
    LOGGER.info("starting show_available_products method")
    with mongo:
        # mongodb database; it all starts here
        db = mongo.connection.HPNorton
        avail_products_dict = {}
        query = {'quantity_available': {'$gt': '1'}}
        for query_results in db.products.find(query):
            key = query_results["product_id"]
            values = {
                "description": query_results["description"],
                "product_type": query_results["product_type"],
                "quantity_available": query_results["quantity_available"]
            }
            temp_dict = {key: values}
            avail_products_dict.update(temp_dict)
    LOGGER.info(f'available products = {avail_products_dict}')
    return avail_products_dict


def show_rentals(product_id):
    """
    Method to show available products
    """
    mongo = MongoDBConnection()
    LOGGER.info("starting show_rentals method")
    with mongo:
        # mongodb database; it all starts here
        db = mongo.connection.HPNorton
        show_rentals_dict = {}
        query = {'product_id': product_id}
        for query_results in db.rentals.find(query):
            query_2 = {'user_id': query_results['user_id']}
            for query_results_2 in db.customers.find(query_2):
                key = query_results_2['user_id']
                value = {
                    'name': query_results_2['name'],
                    'address': query_results_2['address'],
                    'phone_number': query_results_2['phone_number'],
                    'email': query_results_2['email']
                }
                temp_dict = {key: value}
                show_rentals_dict.update(temp_dict)
    LOGGER.info(
        f'showing rentals that match "{product_id}" = {show_rentals_dict}')

    return show_rentals_dict


def drop_data():
    """
    method to drop the data from db
    """
    mongo = MongoDBConnection()
    LOGGER.info("starting drop data method")
    with mongo:
        # mongodb database; it all starts here
        db = mongo.connection.HPNorton
        db.products.drop()
        db.customers.drop()
        db.rentals.drop()


def main():
    """
    main used to call other methods
    """
    
    import_count, error_count = import_data("../data/", "product.csv", "customers.csv", "rental.csv")
    show_available_products()
    show_rentals("prd002")
    drop_data()

if __name__== "__main__":
    main()

