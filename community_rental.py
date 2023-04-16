import datetime

import pymysql
import bcrypt
import tabulate
import decimal

# Prompt user for MySQL username and password
def prompt_user():
    username = input("MySQL username: ")
    password = input("MySQL password: ")

    return username, password


# Prompt user to connect to database using MySQL username/password
def connect_to_database(database):
    # prompt user for MySQL username and password
    username, password = prompt_user()

    try:
        # instantiate connection object to database
        connection = pymysql.connect(host='localhost',
                                     user=username,
                                     password=password,
                                     db=database,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        print("\nYou have successfully logged in to MySQL!")
        return connection

    except pymysql.err.OperationalError as e:
        print('\nError: %d: %s' % (e.args[0], e.args[1]))
        print('\nPlease enter a valid MySQL username and password to access the database.')


# hash password with salt
def hash_password(password):
    # convert password string to byte
    password = bytes(password, 'utf-8')

    # add salt to password
    salt = bcrypt.gensalt()

    # hash the password
    hashed_password = bcrypt.hashpw(password, salt)

    return hashed_password


def check_password(input_password, stored_password):
    # check whether hashed passwords match
    if (bcrypt.checkpw(input_password, stored_password)):
        return True
    else:
        return False


# Prompt to ask user whether they would like to continue or not
def prompt_try_again():
    exit_page = False
    next_steps = ""

    while (not exit_page):
        next_steps = input("\nWould you like to try again (y/n)? ").lower()

        if (next_steps == "n" or next_steps == "y"):
            exit_page = True
        else:
            print("Please enter a valid input: 'y' or 'n'")

    return next_steps


# login function
def login():
    print("\nLog In")

    # prompt user to enter login credentials
    exit_page = False
    while (not exit_page):
        username = input("\nUsername: ")
        password = input("Password: ")

        try:
            # check if username exists
            cursor.callproc("search_user", [username, ])
            if (len(cursor.fetchall()) != 1):
                # username doesn't exist
                print("Entered username does not exist.")

                if (prompt_try_again() == "n"):
                    # user doesn't want to continue - navigate back to sign up/login page
                    return False, None
                else:
                    # user wants to try logging in again
                    continue
            else:
                # username exists, continue by checking to make sure password matches
                # encode inputted password
                input_password = password.encode('utf8')

                # create prepared statement to retrieve stored password for username
                query = "SELECT(get_user_password(%s)) AS password;"
                cursor.execute(query, username)
                stored_password = cursor.fetchone()
                stored_password = stored_password["password"].encode('utf8')

                # check whether passwords match
                if (check_password(input_password, stored_password)):
                    # password matches what's stored in database
                    exit_page = True
                    print("\nYou have successfully logged in! Directing you to the home page...")

                else:
                    # password doesn't match what's stored in database
                    print("Incorrect password for given username.")
                    if (prompt_try_again() == "n"):
                        # user doesn't want to continue - navigate back to sign up/login page
                        return False, None
                    else:
                        # user wants to try logging in again
                        continue

        except pymysql.Error as e:
            # catch any other errors produced by mysql
            print('Error: %d: %s' % (e.args[0], e.args[1]))
            continue

    return True, username


def validate_phone_input(phone):
    if (not phone.isnumeric() or len(phone) > 11):
        print("* Phone number: Must be all numbers and cannot be longer than 11 digits")
        return True
    return False


def validate_address_input(street_num, state, zipcode):
    input_error = False
    if (not street_num.isnumeric()):
        print("* Street number: Must be all numbers")
        input_error = True

    if (len(state) > 2):
        print("* State: Please input the two letter abbreviation for state")
        input_error = True

    if (not zipcode.isnumeric() or len(zipcode) > 5):
        print("* Zipcode: Valid zipcodes are all numbers and are 5 digits long")
        input_error = True
    return input_error


# Validate user input for signing up
def validate_signup_user_input(phone, street_num, state, zipcode):
    # validate phone number
    phone_error = validate_phone_input(phone)

    # validate address
    address_error = validate_address_input(street_num, state, zipcode)

    if (phone_error or address_error):
        return True
    else:
        return False


# sign up function
def signup():
    print("\nSign Up")

    # prompt user for info needed for creating a new user
    exit_page = False
    while (not exit_page):
        username = input("\nUsername: ")
        password = input("Password: ")
        first_name = input("First name: ")
        last_name = input("Last name: ")
        phone = input("Phone number: ")
        street_num = input("Street number: ")
        street_name = input("Street name: ")
        city = input("City: ")
        state = input("State (2 letter abbrev): ")
        zipcode = input("Zipcode: ")
        print()

        # validate user input
        input_error = validate_signup_user_input(phone, street_num, state, zipcode)

        # Errors in input
        if (input_error):
            if (prompt_try_again() == "n"):
                # user doesn't want to continue - navigate back to sign up/login page
                exit_page = True
            else:
                # user wants to try signing up again
                continue

        else:
            # Create new user in user table if no errors in input
            try:
                # hash and salt password before storing
                password = hash_password(password)

                # insert new user to user table (call signup procedure)
                cursor.callproc("signup", [username, password, first_name, last_name, phone, True, False, street_num,
                                           street_name, city, state, zipcode, ])

                # commit the changes
                connection.commit()
                exit_page = True
                print("You have successfully signed up! You may now login with the credentials you signed up with.")

            except pymysql.Error as e:
                if (e.args[0] == 1062):
                    # duplicate username
                    print('Username has already been taken. Please use a different username.')
                else:
                    # catch any other errors produced by mysql
                    print('Error: %d: %s' % (e.args[0], e.args[1]))
                continue
        return


def quit_program():
    print("\nExiting...\nGoodbye!\n")
    connection.close()
    quit()


# Prompt user to sign up or login
def prompt_login_signup():
    successful_login = False
    current_user = None

    # continue prompting user to login or signup
    while (not successful_login):
        print("\nWould you like to:\n1. Log in\n2. Sign up\n3. Quit")
        choice = input("Please select an option: ")

        # convert choice to all lowercase
        choice = choice.lower()

        # allow user to choose by number or by word
        if (choice == "1" or choice == "log in"):
            # navigate to login page
            successful_login, current_user = login()

        elif (choice == "2" or choice == "sign up"):
            # navigate to sign up page
            signup()

        elif (choice == "3" or choice == "quit"):
            # quit program
            quit_program()

        else:
            print("Invalid option. Please enter '1' or 'Log in' to log in, '2' or 'Sign up' to sign up, "
                  "'3' or 'Quit' to exit.")

    return successful_login, current_user


# Retrieve user's basic info from database
def get_user_info(current_user):
    try:
        # call get_user_info procedure to retrieve user's basic info based on username
        cursor.callproc("get_user_info", [current_user, ])
        result = cursor.fetchone()

        return result

    except pymysql.Error as e:
        # catch any errors produced by mysql
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# Retrieve user's payment info from database
def get_user_payment_info(current_user):
    try:
        # get user's stored payment info
        cursor.callproc("get_user_payment_info", [current_user, ])
        result = cursor.fetchall()

        return result

    except pymysql.Error as e:
        # catch any errors produced by mysql
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# Retrieve user's payment preferences from database
def get_user_payment_preference(current_user):
    try:
        # get user's stored payment preferences
        cursor.callproc("get_user_payment_preference", [current_user, ])
        result = cursor.fetchall()

        return result

    except pymysql.Error as e:
        # catch any errors produced by mysql
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# Display all user info (basic info, payment info, and payment preference)
def display_all_user_info(basic_info, payment_info, payment_preference):
    # Basic info: only display username, first name, last name, phone, address
    first_name = basic_info["first_name"]
    last_name = basic_info["last_name"]
    phone = basic_info["phone"]
    street_address = str(basic_info["street_number"]) + " " + basic_info["street_name"]
    city = basic_info["city"]
    state = basic_info["state"]
    zipcode = basic_info["zipcode"]
    print("-- Basic Info --")
    print("First Name: %s\nLast Name: %s\nPhone: %s\nStreet: %s\nCity: %s\nState: %s\nZipcode: %s\n"
          % (first_name, last_name, phone, street_address, city, state, zipcode))

    # Payment info: display user's cc number, expiration date, type (or none if no payment info exists)
    print("-- Payment Info --")
    if (len(payment_info) == 0):
        print("None\n")
    else:
        for i in range(len(payment_info)):
            cc_number = payment_info[i]["cc_number"]
            expiration_date = payment_info[i]["expiration_date"]
            cc_type = payment_info[i]["type"]
            print("%d) CC Number: %s\tExpiration Date: %s\tType: %s" % (i + 1, cc_number, expiration_date, cc_type))

    # Payment preference: display cc types the user prefers (or none if no payment preference exists)
    print("\n-- Payment Preference --")
    if (len(payment_preference) == 0):
        print("None\n")
    else:
        for i in range(len(payment_preference)):
            preferred_type = payment_preference[i]["type"]
            print("%d) %s" % (i + 1, preferred_type))


# Retrieve and display user info from database
def user_info(current_user):
    # Retrieve user's basic info
    basic_info = get_user_info(current_user)

    # Retrieve user's payment info
    payment_info = get_user_payment_info(current_user)

    # Retrieve user's payment preferences
    payment_preference = get_user_payment_preference(current_user)

    # Display all user info
    display_all_user_info(basic_info, payment_info, payment_preference)


def update_user_name(current_user):
    # Get new first and last name from user input
    print("\n-- Update Name --")
    new_first_name = input("First name: ")
    new_last_name = input("Last name: ")

    try:
        # update user's first name in database
        cursor.callproc("update_user_first_name", [current_user, new_first_name, ])

        # update user's last name in database
        cursor.callproc("update_user_last_name", [current_user, new_last_name, ])

        # commit updated data
        connection.commit()

        # update success and show new updated values
        print("\nName successfully updated!\n")
        user_info(current_user)

    except pymysql.Error as e:
        # catch any errors produced by mysql
        print('Error: %d: %s' % (e.args[0], e.args[1]))


def update_phone(current_user):
    input_error = True

    # Get new phone number from user input
    print("\n-- Update Phone Number --")

    while (input_error):
        new_phone = input("New phone: ")
        input_error = validate_phone_input(new_phone)

    try:
        # update user's phone number in database
        cursor.callproc("update_user_phone", [current_user, new_phone, ])

        # commit updated data
        connection.commit()

        # update success and show new updated values
        print("\nPhone number successfully updated!\n")
        user_info(current_user)

    except pymysql.Error as e:
        # catch any errors produced by mysql
        print('Error: %d: %s' % (e.args[0], e.args[1]))


def update_address(current_user):
    input_error = True
    print("\n-- Update Address --")

    # Get new address from user input
    while (input_error):
        new_street_num = input("New street number: ")
        new_street_name = input("New street name: ")
        new_city = input("New city: ")
        new_state = input("New state: ")
        new_zipcode = input("New zipcode: ")
        input_error = validate_address_input(new_street_num, new_state, new_zipcode)

    try:
        # update user's address in database
        cursor.callproc("update_user_address", [current_user, new_street_num, new_street_name, new_city, new_state,
                                                new_zipcode, ])

        # commit updated data
        connection.commit()

        # update success and show new updated values
        print("\nAddress successfully updated!\n")
        user_info(current_user)

    except pymysql.Error as e:
        # catch any errors produced by mysql
        print('Error: %d: %s' % (e.args[0], e.args[1]))


def validate_cc_type(cc_type):
    if (cc_type.upper() != "VISA" and cc_type.upper() != "AMERICAN EXPRESS" and cc_type.upper() != "MASTERCARD"):
        print("* Credit card type: Must be Visa, American Express, or Mastercard")
        return True
    return False


def validate_cc_info(cc_number, expiration_date, cc_type):
    input_error = False

    # validate credit card number
    if (len(cc_number) > 16 or not cc_number.isnumeric()):
        print("* Credit card number: Must be all numbers and no more than 16 digits")
        input_error = True

    # validate expiration date
    try:
        datetime.date.fromisoformat(expiration_date)
    except ValueError:
        print("* Expiration date: Must be in the format YYYY-MM-DD")
        input_error = True

    # validate credit card type
    type_error = validate_cc_type(cc_type)

    if (input_error or type_error):
        return True
    return False


def create_payment_info(current_user):
    input_error = True
    print("\n-- Add Payment Info --")

    # Get credit card info from user
    while (input_error):
        cc_number = input("Credit card #: ")
        expiration_date = input("Expiration date (YYYY-MM-DD): ")
        cc_type = input("Credit card type (Visa, Mastercard, American Express): ")
        input_error = validate_cc_info(cc_number, expiration_date, cc_type)

    try:
        # add new payment info to database and associate with user
        cursor.callproc("user_adds_payment_info", [current_user, cc_number, expiration_date, cc_type, ])

        # commit updated data
        connection.commit()

        # update success and show new updated values
        print("\nPayment info successfully added!\n")
        user_info(current_user)
        return cc_number

    except pymysql.Error as e:
        # catch any errors produced by mysql
        print('Error: %d: %s' % (e.args[0], e.args[1]))


def delete_payment_info(current_user):
    # Get credit card info from user
    print("\n-- Delete Payment Info --")
    cc_number = input("Enter the credit card # you would like to delete: ")

    try:
        # delete user association with payment info from database
        cursor.callproc("user_deletes_payment_info", [current_user, cc_number, ])

        # commit updated data
        connection.commit()

        # update success and show new updated values
        print("\nPayment info deleted!\n")
        user_info(current_user)

    except pymysql.Error as e:
        # catch any errors produced by mysql
        print('Error: %d: %s' % (e.args[0], e.args[1]))


def create_payment_preference(current_user):
    input_error = True
    print("\n-- Add Payment Preference --")

    try:
        # check to make sure user is seller
        seller_query = "SELECT (user_is_seller(%s)) AS seller;"
        cursor.execute(seller_query, current_user)
        is_seller = cursor.fetchone()

        if (is_seller["seller"]):
            # user is seller - can add payment preference
            # Get payment preference from user
            while (input_error):
                cc_type = input("Credit card type preference (Visa, Mastercard, American Express): ")
                input_error = validate_cc_type(cc_type)

            try:
                # add user's payment preference to database
                cursor.callproc("user_adds_payment_preference", [current_user, cc_type, ])

                # commit updated data
                connection.commit()

                # update success and show new updated values
                print("\nPayment preference successfully added!\n")
                user_info(current_user)

            except pymysql.Error as e:
                # catch any errors produced by mysql
                print('Error: %d: %s' % (e.args[0], e.args[1]))

        else:
            # user is not seller - cannot add payment preference until they create a listing to become a seller
            print("Sorry, you are not a seller. Please create a listing to become a seller before adding "
                  "a payment preference.")

    except pymysql.Error as e:
        # catch any errors produced by mysql
        print('Error: %d: %s' % (e.args[0], e.args[1]))


def delete_payment_preference(current_user):
    # Get cc type to be deleted from payment preference
    print("\n-- Delete Payment Preference --")
    cc_type = input("Enter the credit card type you no longer prefer: ")

    try:
        # delete user association with payment preference from database
        cursor.callproc("user_deletes_payment_preference", [current_user, cc_type, ])

        # commit updated data
        connection.commit()

        # update success and show new updated values
        print("\nPayment preference deleted!\n")
        user_info(current_user)

    except pymysql.Error as e:
        # catch any errors produced by mysql
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# Menu options for profile page
def display_profile_menu_options():
    print("\nWhat would you like to do?")
    print("1. Update name\n2. Update phone number\n3. Update address\n4. Add new payment info\n"
          "5. Delete payment info\n6. Add new payment preference\n7. Delete payment preference\n8. Exit profile")


def choose_profile_menu_option(current_user):
    # Prompt user to choose a profile menu option until choose exit profile
    exit_profile = False
    while (not exit_profile):
        display_profile_menu_options()
        selection = input("Choose an option #: ")

        if (selection == "1"):
            # Update first and last name
            update_user_name(current_user)

        elif (selection == "2"):
            # Update phone number
            update_phone(current_user)

        elif (selection == "3"):
            # Update address
            update_address(current_user)

        elif (selection == "4"):
            # Add new payment info
            create_payment_info(current_user)

        elif (selection == "5"):
            # Delete payment info
            delete_payment_info(current_user)

        elif (selection == "6"):
            # Add new payment preference
            create_payment_preference(current_user)

        elif (selection == "7"):
            # Delete payment preference
            delete_payment_preference(current_user)

        elif (selection == "8"):
            # exit profile page - return to home
            exit_profile = True

        else:
            # Invalid selection - prompt user to choose again
            print("Invalid option. Please choose a number that corresponds to a menu option.")


def profile(current_user):
    print("\n%s's Profile\n" % current_user)

    # Retrieve and display user's basic info, payment info, and payment preferences
    user_info(current_user)

    # Display menu options for profile page
    choose_profile_menu_option(current_user)


# Retrieve user's listings from database
def get_user_listings(current_user):
    try:
        # call procedure to retrieve user's listings
        cursor.callproc("get_user_listings", [current_user, ])
        result = cursor.fetchall()

        return result

    except pymysql.Error as e:
        # catch any errors produced by mysql
        print('Error: %d: %s' % (e.args[0], e.args[1]))


def display_user_listings(user_listings):
    # Display user's listings including item description, price, quantity, average_rating, and category
    if (len(user_listings) == 0):
        # User does not have any listings
        print("You currently do not have any listings")
    else:
        # User has listings
        for i in range(len(user_listings)):
            description = user_listings[i]["description"]
            price = user_listings[i]["price"]
            quantity = str(user_listings[i]["quantity"])
            avg_rating = user_listings[i]["average_rating"]
            rating_count = user_listings[i]["rating_count"]
            category = user_listings[i]["category"]

            if (rating_count == 0):
                # Rating is none when there have been no ratings yet
                print("%d) Item description: %s\tPrice: $%s\tQuantity: %s\tRating: None\tCategory: %s" %
                      (i + 1, description, price, quantity, category))
            else:
                # Include rating # when there have been ratings
                print("%d) Item description: %s\tPrice: $%s\tQuantity: %s\tRating: %s\tCategory: %s" %
                      (i + 1, description, price, quantity, avg_rating, category))


def user_listings(current_user):
    # Retrieve user's listings from database
    results = get_user_listings(current_user)

    # Display user's listings
    display_user_listings(results)

    return results


# validate input for listing price and quantity, and item description before adding/updating database
def validate_price_quantity_description(price, quantity, description):
    price_error = False
    quantity_error = False
    description_error = False

    # validate price
    try:
        # check for 2 decimal places
        if (not len(price.rsplit('.')[-1]) == 2):
            price_error = True

        # check for price not longer than 13 digits
        if (len(price) > 13):
            price_error = True

        # check price is a number
        price = float(price)

        # check price is not negative
        if (price < 0):
            price_error = True

        if (price_error):
            print("* Price: Must be a number with no more than 13 digits and must include 2 decimal places")

    except ValueError:
        print("* Price: Must be a number with no more than 13 digits and must include 2 decimal places")
        price_error = True

    # validate quantity
    if (not quantity.isnumeric()):
        print("* Quantity: Must be a number")
        quantity_error = True

    # validate description
    if (len(description) > 1000):
        print("* Description: Too long. Please shorten the description")
        description_error = True

    if (price_error or quantity_error or description_error):
        return True
    return False


# create listing in database with new item
def create_new_item_listing(current_user, description, category, price, quantity):
    try:
        # create listing and item in database
        cursor.callproc("create_new_item_listing", [current_user, description, category, price, quantity, ])

        # commit inserted data
        connection.commit()

        # update success and show new updated listings
        print("\nListing successfully created!\n")
        print("\n-- %s's Listings --" % current_user)
        user_listings(current_user)
        print()

    except pymysql.Error as e:
        # catch any errors produced by mysql
        print('Error: %d: %s' % (e.args[0], e.args[1]))


def create_new_item_listing_page(current_user):
    # prompt user for item and listing attributes
    input_error = True
    while (input_error):
        print("\n-- Create Listing For New Item --")
        description = input("Item description: ")
        category = input("Item category: ")
        price = input("Item price: ")
        quantity = input("Quantity of items: ")
        input_error = validate_price_quantity_description(price, quantity, description)

        # check if user wants to continue
        if (input_error):
            option = prompt_try_again()

            if (option == "n"):
                return

    # create new listing and new item in database
    create_new_item_listing(current_user, description, category, price, quantity)


# retrieve all items owned by user from database
def get_user_items(current_user):
    try:
        # retrieve user's items from database
        cursor.callproc("search_items_by_seller", [current_user, ])
        result = cursor.fetchall()

        return result

    except pymysql.Error as e:
        # catch any errors produced by mysql
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# filter items owned by user retrieved from database to only include items that aren't part of a listing
def get_unlisted_user_items(current_user):
    # get items owned by user from database
    items = get_user_items(current_user)

    # get currently active listings for user from database
    listings = get_user_listings(current_user)

    # create list to only include item id that are part of active listings
    listings_by_item = []
    for i in range(len(listings)):
        listings_by_item.append(listings[i].get("item"))

    # filter items that aren't part of any listings to filtered_items list
    filtered_items = []
    for each in items:
        if (each.get("id") not in listings_by_item):
            filtered_items.append(each)

    return filtered_items


# Display all items owned by user that aren't part of any active listings
def display_inactive_items(filtered_items):
    for i in range(len(filtered_items)):
        description = filtered_items[i]["description"]
        avg_rating = filtered_items[i]["average_rating"]
        rating_count = filtered_items[i]["rating_count"]
        category = filtered_items[i]["category"]

        if (rating_count == 0):
            # Rating is none when there have been no ratings yet
            print("%d) Item description: %s\tRating: None\tCategory: %s" %
                  (i + 1, description, category))
        else:
            # Include rating # when there have been ratings
            print("%d) Item description: %s\tRating: %s\tCategory: %s" %
                  (i + 1, description, avg_rating, category))


def prompt_listing_attributes():
    # prompt user for listing attributes
    input_error = True
    while (input_error):
        price = input("Price: ")
        quantity = input("Quantity of items: ")
        input_error = validate_price_quantity_description(price, quantity, "")

    return price, quantity


def create_existing_item_listing(current_user, item, price, quantity):
    item_id = item.get("id")

    try:
        # create listing from existing item in database
        cursor.callproc("create_listing", [current_user,  item_id, price, quantity])

        # commit inserted data
        connection.commit()

        # update success and show new updated listings
        print("\nListing successfully created!\n")
        print("\n-- %s's Listings --" % current_user)
        user_listings(current_user)
        print()

    except pymysql.Error as e:
        # catch any errors produced by mysql
        print('Error: %d: %s' % (e.args[0], e.args[1]))


def create_existing_item_listing_page(current_user):
    print("\n-- Create Listing For Existing Item --")

    # check whether user has any items that aren't part of any listings
    filtered_items = get_unlisted_user_items(current_user)

    if (len(filtered_items) == 0):
        # user doesn't have any items that aren't part of listings - cannot create any listings from existing items
        print("Sorry, you currently don't have any items that aren't part of any active listings. "
              "Please create a new listing for a new item or update an active listing for any existing items\n")
    else:
        # user has items that aren't part of any listings - prompt user to choose one to create a listing for
        valid_item = False
        while (not valid_item):
            print("Which item would you like to create a listing for?")

            # Retrieve and display user's items that aren't part of any active listings
            display_inactive_items(filtered_items)

            selection = input("\nChoose an option # from the above items ('Q' to exit): ")

            if (selection.lower() == "q"):
                print()
                return
            elif (not selection.isnumeric()):
                print("Invalid option. Please choose a number from the given list\n")
            else:
                selection = int(selection) - 1

                # validate selection
                if (selection >= len(filtered_items) or selection < 0):
                    # invalid selection
                    print("Invalid option. Please choose a valid option number from the given list\n")
                else:
                    # valid selection - create listing for item
                    price, quantity = prompt_listing_attributes()
                    create_existing_item_listing(current_user, filtered_items[selection], price, quantity)
                    valid_item = True


# menu options for create listing page
def create_listing_menu_options():
    print("What kind of listing would you like to create?")
    print("1. Create listing for new item\n2. Create listing for existing item\n3. Exit")


def choose_create_listing_menu_option(current_user):
    # Prompt user to choose a create listings menu option until choose exit
    exit_create_listings = False
    while (not exit_create_listings):
        create_listing_menu_options()
        selection = input("Choose an option #: ")

        if (selection == "1"):
            # navigate to create listing for new item
            create_new_item_listing_page(current_user)

        elif (selection == "2"):
            # navigate to create listing for existing item
            create_existing_item_listing_page(current_user)

        elif (selection == "3"):
            # exit create listings page - return to manage listings
            exit_create_listings = True

            # show user's listings
            print("\n-- %s's Listings --" % current_user)
            user_listings(current_user)

        else:
            # Invalid selection - prompt user to choose again
            print("Invalid option. Please choose a number that corresponds to a menu option.")

def create_listing_page(current_user):
    print("\n-- Create Listing --")

    # menu options - create listing on new or existing item
    choose_create_listing_menu_option(current_user)


# prompt user for new price, quantity, and item description to update listing
def update_listing_values():
    input_error = True

    while (input_error):
        price = input("\nNew price: ")
        quantity = input("New quantity: ")
        description = input("New description: ")
        input_error = validate_price_quantity_description(price, quantity, description)

    return price, quantity, description


# update price, quantity, and description for listing in database
def update_listing(current_user, listing, new_price, new_quantity, new_description):
    # get item id associated to listing
    item = listing.get("item")

    try:
        # update listing in database
        cursor.callproc("update_listing", [item, current_user, new_price, new_quantity, new_description, ])

        # commit updated data
        connection.commit()

        # update success and show new updated listings
        print("\nListing successfully updated!\n")
        print("\n-- %s's Listings --" % current_user)
        user_listings(current_user)

    except pymysql.Error as e:
        # catch any errors produced by mysql
        print('Error: %d: %s' % (e.args[0], e.args[1]))


def update_listing_page(current_user):
    print("\n-- Update Listing --")

    # check whether user has any listings before asking to choose listing to update
    num_listings = get_user_listings(current_user)

    if (len(num_listings) == 0):
        # user doesn't have any listings - cannot update
        print("Sorry, you currently don't have any listings to update")
    else:
        # user has listings - prompt user to choose one to update
        valid_listing = False
        while (not valid_listing):
            print("Which listing would you like to update?")

            # Retrieve and display user's listings
            listings = user_listings(current_user)

            selection = input("\nChoose listing # from the above options ('Q' to exit): ")

            if (selection.lower() == "q"):
                print()
                return
            elif (not selection.isnumeric()):
                print("Invalid option. Please choose a valid listing number from the options\n")
            else:
                selection = int(selection) - 1

                # validate selection
                if (selection >= len(listings) or selection < 0):
                    # invalid selection
                    print("Invalid listing number. Please choose a valid listing number from the options\n")
                else:
                    # valid selection - update chosen listing
                    new_price, new_quantity, new_description = update_listing_values()
                    update_listing(current_user, listings[selection], new_price, new_quantity, new_description)
                    valid_listing = True


# delete listing from database
def delete_listing(current_user, listing):
    # get item id associated to listing
    item = listing.get("item")

    try:
        # delete listing from database
        cursor.callproc("delete_listing", [item, current_user, ])

        # commit deleted data
        connection.commit()

        # update success and show current listings
        print("\nListing successfully deleted!\n")
        print("\n-- %s's Listings --" % current_user)
        user_listings(current_user)

    except pymysql.Error as e:
        # catch any errors produced by mysql
        print('Error: %d: %s' % (e.args[0], e.args[1]))


def delete_listing_page(current_user):
    print("\n-- Delete Listing --")

    # check whether user has any listings before asking to choose listing to delete
    num_listings = get_user_listings(current_user)

    if (len(num_listings) == 0):
        # user doesn't have any listings - cannot delete any
        print("Sorry, you currently don't have any listings to delete")
    else:
        # user has listings - prompt user to choose one to delete
        valid_listing = False
        while (not valid_listing):
            print("Which listing would you like to delete?")

            # Retrieve and display user's listings
            listings = user_listings(current_user)

            selection = input("\nChoose listing # from the above options ('Q' to quit): ")

            if (selection.lower() == "q"):
                print()
                return
            elif (not selection.isnumeric()):
                print("Invalid option. Please choose a number from the given list\n")
            else:
                selection = int(selection) - 1

                # validate selection
                if (selection >= len(listings) or selection < 0):
                    # invalid selection
                    print("Invalid listing number. Please choose a valid listing number from the options\n")
                else:
                    # valid selection - delete chosen listing
                    delete_listing(current_user, listings[selection])
                    valid_listing = True


# Menu options for listings page
def display_listings_menu_options():
    print("\nWhat would you like to do?")
    print("1. Create listing\n2. Update listing\n3. Delete listing\n4. Exit listings")


def choose_listings_menu_option(current_user):
    # Prompt user to choose a listings menu option until choose exit listings
    exit_listings = False
    while (not exit_listings):
        display_listings_menu_options()
        selection = input("Choose an option #: ")

        if (selection == "1"):
            # navigate to create listing page
            create_listing_page(current_user)

        elif (selection == "2"):
            # navigate to update listing page
            update_listing_page(current_user)

        elif (selection == "3"):
            # navigate to delete listing page
            delete_listing_page(current_user)

        elif (selection == "4"):
            # exit listings page - return to home
            exit_listings = True

        else:
            # Invalid selection - prompt user to choose again
            print("Invalid option. Please choose a number that corresponds to a menu option.")


def listings_page(current_user):
    print("\n-- %s's Listings --" % current_user)

    # Retrieve and display user's listings
    user_listings(current_user)

    # Display menu options for listings page
    choose_listings_menu_option(current_user)


# print table (tabulate):
def print_table(rows, keys):
    print(tabulate.tabulate(rows, keys, tablefmt='grid'))


# list all items
def all_items():
    try:
        cursor.callproc('all_items')
        items = cursor.fetchall()
        desired_keys = ['id', 'owner', 'description', 'category', 'average_rating']
        rows = []
        for item in items:
            rows.append([item.get(k) for k in desired_keys])
        for row in rows:
            for i in range(len(row)):
                if row[i] == decimal.Decimal('0.0'):
                    row[i] = "None"
        print("\n-- All items --")
        print_table(rows, desired_keys)
        print(rows)
        return items

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# list all item categories
def all_item_categories():
    try:
        cursor.callproc('all_categories')
        categories = cursor.fetchall()
        desired_keys = ['category']
        rows = []
        for category in categories:
            rows.append([category.get(k) for k in desired_keys])
        for row in rows:
            for i in range(len(row)):
                if row[i] == decimal.Decimal('0.0'):
                    row[i] = "None"
        print("\n-- All Categories --")
        print_table(rows, desired_keys)
        return categories

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# search for item by category
def search_items_by_category():
    all_item_categories()
    category = ""
    while category == "":
        category = input("What item category would you like to search for?\n")

    try:
        cursor.callproc('search_items_by_category', [category])
        items = cursor.fetchall()
        desired_keys = ['id', 'owner', 'description', 'category', 'average_rating']
        rows = []
        for item in items:
            rows.append([item.get(k) for k in desired_keys])
        for row in rows:
            for i in range(len(row)):
                if row[i] == decimal.Decimal('0.0'):
                    row[i] = "None"
        print("\n-- Items found matching the '" + category + "' category --")
        print_table(rows, desired_keys)
        return items

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# list all users
def all_users():
    try:
        cursor.callproc('all_users')
        users = cursor.fetchall()
        desired_keys = ['username', 'first_name', 'last_name', 'phone', 'average_rating',
                        'street_number', 'street_name', 'city', 'state', 'zipcode']
        rows = []
        for user in users:
            rows.append([user.get(k) for k in desired_keys])
        for row in rows:
            for i in range(len(row)):
                if row[i] == decimal.Decimal('0.0'):
                    row[i] = "None"
        print("\n-- All Users --")
        print_table(rows, desired_keys)
        return users

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# search for item by owner
def search_items_by_owner():
    all_users()
    owner = ""
    while owner == "":
        owner = input("Whose items would you like to search for? (username)\n")
    try:
        cursor.callproc('search_items_by_seller', [owner])
        items = cursor.fetchall()
        desired_keys = ['id', 'owner', 'description', 'category', 'average_rating']
        rows = []
        for item in items:
            rows.append([item.get(k) for k in desired_keys])
        for row in rows:
            for i in range(len(row)):
                if row[i] == decimal.Decimal('0.0'):
                    row[i] = "None"
        print("\n-- Items owned by '" + owner + "' --")
        print_table(rows, desired_keys)
        return items

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# search for item by id
def search_item_by_id():
    item_id = 0
    while item_id <= 0:
        item_id = input("What item ID would you like to search for?\n")
    try:
        cursor.callproc('search_item_by_id', [item_id])
        items = cursor.fetchall()
        desired_keys = ['id', 'owner', 'description', 'category', 'average_rating']
        rows = []
        for item in items:
            rows.append([item.get(k) for k in desired_keys])
        for row in rows:
            for i in range(len(row)):
                if row[i] == decimal.Decimal('0.0'):
                    row[i] = "None"
        print("\n-- Searching for item with ID '" + item_id + "' --")
        print_table(rows, desired_keys)
        return items

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# search for item by id
def search_item(item_id):
    try:
        cursor.callproc('search_item_by_id', [item_id])
        items = cursor.fetchall()
        desired_keys = ['id', 'owner', 'description', 'category', 'average_rating']
        rows = []
        for item in items:
            rows.append([item.get(k) for k in desired_keys])
        for row in rows:
            for i in range(len(row)):
                if row[i] == decimal.Decimal('0.0'):
                    row[i] = "None"
        print("\n")
        print_table(rows, desired_keys)
        return items

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# list all listings
def all_listings():
    try:
        cursor.callproc('all_listings')
        listings = cursor.fetchall()
        desired_keys = ['item', 'owner', 'description', 'category', 'average_rating',
                        'price', 'quantity']
        rows = []
        for listing in listings:
            rows.append([listing.get(k) for k in desired_keys])
        for row in rows:
            for i in range(len(row)):
                if row[i] == decimal.Decimal('0.0'):
                    row[i] = "None"
        print("\n-- All Listings --")
        print_table(rows, desired_keys)
        return listings

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# list all rentals
def all_rentals():
    try:
        cursor.callproc('all_rentals')
        rentals = cursor.fetchall()
        desired_keys = ['item', 'owner', 'customer', 'description', 'category',
                        'average_rating', 'rental_date', 'return_date']
        rows = []
        for rental in rentals:
            rows.append([rental.get(k) for k in desired_keys])
        for row in rows:
            for i in range(len(row)):
                if row[i] == decimal.Decimal('0.0'):
                    row[i] = "None"
        print("\n-- All Rentals --")
        print_table(rows, desired_keys)
        return rentals

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# rate item
def rate_item(current):
    try:
        print("\n-- Rating an item --")
        all_items()
        item = input("Which item would you like to rate? (item ID)\n")
        rating = input("What would you rate this item from 1-5?\n")
        cursor.callproc('rate_item', [current, item, rating])
        print("\nItem " + item + " given a rating of " + rating + "\n")
        search_item(item)

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# get user's payment info
def get_user_payment(user):
    try:
        cursor.callproc('get_user_payment_info', [user])
        payments = cursor.fetchall()
        desired_keys = ['cc_number', 'expiration_date']
        rows = []
        for payment in payments:
            rows.append([payment.get(k) for k in desired_keys])
        for row in rows:
            for i in range(len(row)):
                if row[i] == decimal.Decimal('0.0'):
                    row[i] = "None"
        print("\n-- Your current payment info --")
        print_table(rows, desired_keys)

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


def choose_payment(current):
    get_user_payment(current)
    while True:
        print("Do you want to use an existing payment or create a new one?\n"
              "1. Select from an existing payment\n"
              "2. Create a new payment method")
        answer = input("Select an option #: ")
        if answer == "1":
            payment = input("Select a credit card number to use: ")
            break
        elif answer == "2":
            payment = create_payment_info(current)
            break
        else:
            print("Please select a valid option.")
    return payment


# get specified user's rentals
def get_rentals(current):
    try:
        cursor.callproc('get_rentals', [current])
        rentals = cursor.fetchall()
        desired_keys = ['item', 'owner', 'customer', 'description', 'category',
                        'average_rating', 'rental_date', 'return_date']
        rows = []
        for rental in rentals:
            rows.append([rental.get(k) for k in desired_keys])
        for row in rows:
            for i in range(len(row)):
                if row[i] == decimal.Decimal('0.0'):
                    row[i] = "None"
        print("\n-- Items currently rented by user '" + current + "' --")
        print_table(rows, desired_keys)
        return rentals
    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# rent an item
def rent_item(current):
    try:
        print("\n-- Renting an item --")
        all_listings()
        item = input("Which item would you like to rent? (item ID)\n")
        payment = choose_payment(current)
        rental_date = input("When are you renting this item? (YYYY-MM-DD):\n")
        return_date = input("When are you returning this item? (YYYY-MM-DD):\n")
        cursor.callproc('rent_item', [item, current, payment, rental_date, return_date])
        print("\nItem rental successful!\n")
        get_rentals(current)

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


def item_search_page(current):
    while True:
        print("\n-- Item Search --")
        print("What would you like to do?")
        print("1. List all items\n"
              "2. List all item categories\n"
              "3. Search for items by category\n"
              "4. Search for items by owner\n"
              "5. Rate item\n"
              "6. Rent item\n"
              "7. List all items currently rented out\n"
              "8. Exit item search")
        option = input("Choose an option #: ")
        if option == "1":
            all_items()
        elif option == "2":
            all_item_categories()
        elif option == "3":
            search_items_by_category()
        elif option == "4":
            search_items_by_owner()
        elif option == "5":
            rate_item(current)
        elif option == "6":
            rent_item(current)
        elif option == "7":
            all_rentals()
        elif option == "8":
            break
        else:
            print("Invalid option. Please choose a number that corresponds to a menu option.")


# list all sellers
def all_sellers():
    try:
        cursor.callproc('all_sellers')
        sellers = cursor.fetchall()
        desired_keys = ['username', 'first_name', 'last_name', 'phone', 'average_rating',
                        'street_number', 'street_name', 'city', 'state', 'zipcode']
        rows = []
        for seller in sellers:
            rows.append([seller.get(k) for k in desired_keys])
        for row in rows:
            for i in range(len(row)):
                if row[i] == decimal.Decimal('0.0'):
                    row[i] = "None"
        print("\n-- All Sellers --")
        print_table(rows, desired_keys)
        return sellers

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# search for user by username/firstname/lastname
def search_user():
    name = ""
    while name == "":
        name = input("Who would you like to search for?\n")
    try:
        cursor.callproc('search_user', [name])
        users = cursor.fetchall()
        desired_keys = ['username', 'first_name', 'last_name', 'phone', 'average_rating',
                        'street_number', 'street_name', 'city', 'state', 'zipcode']
        rows = []
        for user in users:
            rows.append([user.get(k) for k in desired_keys])
        for row in rows:
            for i in range(len(row)):
                if row[i] == decimal.Decimal('0.0'):
                    row[i] = "None"
        print("\n-- Users found matching the name '" + name + "' --")
        print_table(rows, desired_keys)
        return users

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# search specific user
def search_specific_user(name):
    try:
        cursor.callproc('search_user', [name])
        users = cursor.fetchall()
        desired_keys = ['username', 'first_name', 'last_name', 'phone', 'average_rating',
                        'street_number', 'street_name', 'city', 'state', 'zipcode']
        rows = []
        for user in users:
            rows.append([user.get(k) for k in desired_keys])
        for row in rows:
            for i in range(len(row)):
                if row[i] == decimal.Decimal('0.0'):
                    row[i] = "None"
        print("\n")
        print_table(rows, desired_keys)
        return users

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# rate user
def rate_user(current):
    try:
        print("\n-- Rating a user --")
        all_users()
        username = input("Which user (username) would you like to rate?\n")
        rating = input("What would you rate this user from 1-5?\n")
        cursor.callproc('rate_user', [current, username, rating])
        print("\n User '" + username + "' given a rating of " + rating + "\n")
        search_specific_user(username)
        return

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


def user_search_page(current):
    while True:
        print("\n-- User Search --")
        print("What would you like to do?")
        print("1. List all users\n"
              "2. List all sellers\n"
              "3. Search for user by name\n"
              "4. Rate user\n"
              "5. Exit item search")
        option = input("Choose an option #: ")
        if option == "1":
            all_users()
        elif option == "2":
            all_sellers()
        elif option == "3":
            search_user()
        elif option == "4":
            rate_user(current)
        elif option == "5":
            break
        else:
            print("Invalid option. Please choose a number that corresponds to a menu option.")


# list all customers
def all_customers():
    try:
        cursor.callproc('all_customers')
        customers = cursor.fetchall()
        desired_keys = ['username', 'first_name', 'last_name', 'phone', 'average_rating',
                        'street_number', 'street_name', 'city', 'state', 'zipcode']
        rows = []
        for customer in customers:
            rows.append([customer.get(k) for k in desired_keys])
        for row in rows:
            for i in range(len(row)):
                if row[i] == decimal.Decimal('0.0'):
                    row[i] = "None"
        print("\n-- All Customers --")
        print_table(rows, desired_keys)
        return customers

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# get user wishlist
def get_wishlist(current):
    try:
        cursor.callproc('list_wishlist', [current])
        wishlist = cursor.fetchall()
        desired_keys = ['item', 'description', 'category']
        rows = []
        for item in wishlist:
            rows.append([item.get(k) for k in desired_keys])
        for row in rows:
            for i in range(len(row)):
                if row[i] == decimal.Decimal('0.0'):
                    row[i] = "None"
        print("\n-- All items on your wishlist --")
        print_table(rows, desired_keys)
        return wishlist

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# add item to wishlist
def add_wishlist(customer):
    try:
        print("\n-- Adding an item to your wishlist --")
        get_wishlist(customer)
        all_items()
        item = input("Which item would you like to add to your wishlist? (item ID)\n")
        cursor.callproc('wish_for_item', [customer, item])
        get_wishlist(customer)
        return

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# delete item from wishlist
def delete_wishlist(customer):
    try:
        print("\n-- Deleting an item from your wishlist --")
        get_wishlist(customer)
        item = input("Which item would you like to delete from your wishlist? (item ID)\n")
        cursor.callproc('delete_wishlist_item', [customer, item])
        get_wishlist(customer)
        return

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# look up a wishlist
def search_wishlist():
    customer = ""
    while customer == "":
        all_customers()
        customer = input("Whose wishlist would you like to search for? (username)\n")
    try:
        cursor.callproc('list_wishlist', [customer])
        wishlist = cursor.fetchall()
        desired_keys = ['item', 'description', 'category']
        rows = []
        for item in wishlist:
            rows.append([item.get(k) for k in desired_keys])
        for row in rows:
            for i in range(len(row)):
                if row[i] == decimal.Decimal('0.0'):
                    row[i] = "None"
        print("\n-- All items on '" + customer + "''s wishlist --")
        print_table(rows, desired_keys)
        return wishlist

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


def wishlist_page(current):
    while True:
        print("\n-- Manage Wishlist --")
        print("What would you like to do?")
        print("1. View your own wishlist\n"
              "2. Add an item to your wishlist\n"
              "3. Delete an item from your wishlist\n"
              "4. View another user's wishlist\n"
              "5. Exit item search")
        option = input("Choose an option #: ")
        if option == "1":
            get_wishlist(current)
        elif option == "2":
            add_wishlist(current)
        elif option == "3":
            delete_wishlist(current)
        elif option == "4":
            search_wishlist()
        elif option == "5":
            break
        else:
            print("Invalid option. Please choose a number that corresponds to a menu option.")


# Menu options for home page after log in
def display_menu_options():
    print("\n-- Community Rentals Home --")
    print("What would you like to do?")
    print("1. Profile\n2. Manage listings\n3. Search for items\n4. Search for user\n5. Manage wishlist\n6. Log out")


def home_menu(current_user):
    logout = False

    # menu of options
    while (not logout):
        display_menu_options()
        selection = input("Choose an option #: ")

        if (selection == "1"):
            # navigate to profile page
            profile(current_user)

        elif (selection == "2"):
            # navigate to manage listings page
            listings_page(current_user)

        elif (selection == "3"):
            # navigate to search for items page
            item_search_page(current_user)

        elif (selection == "4"):
            # navigate to search for users page
            user_search_page(current_user)

        elif (selection == "5"):
            # navigate to manage wishlist page
            wishlist_page(current_user)

        elif (selection == "6"):
            # navigate back to log in screen
            logout = True

        else:
            # Invalid selection - prompt user to choose again
            print("Invalid option. Please choose a number that corresponds to a menu option.")
    return


def start_community_rentals_app():
    # welcome message
    print("\nWelcome to the Community Rentals App!")

    # prompt user to log in or signup
    successful_login, current_user = prompt_login_signup()

    # navigate to home page if login successful
    if (successful_login and current_user != None):
        print("\nWelcome, " + current_user + "!")
        home_menu(current_user)

    # exit program
    quit_program()


if __name__ == '__main__':
    database = "community_rentals"
    connection = None

    # prompt user for valid username/password to connect to database
    print("\nPlease enter your MySQL username and password to access the database.")
    while (connection == None):
        connection = connect_to_database(database)

    # instantiate cursor for connection
    cursor = connection.cursor()

    # begin Community Rentals App
    print("\nDirecting you to the Community Rentals Application...")
    start_community_rentals_app()

    # close connection
    connection.close()
