def load_rentals_file(filename):
    with open(filename, 'r') as file:
        try:
            # first I read the file into a variable. Don’t care about json (yet)
            file_content = file.read()

        # note how I print the exception so it doesn’t fail silently
        except Exception as e:
            print(e)

    # now I convert a string variable to json
    data = json.loads(file_content)
    return data
