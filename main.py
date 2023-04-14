import datetime

import pymysql
import bcrypt

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
            # instantiate cursor for connection
            cursor = connection.cursor()

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
                # instantiate cursor for connection
                cursor = connection.cursor()

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
        # instantiate cursor for connection
        cursor = connection.cursor()

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
        # instantiate cursor for connection
        cursor = connection.cursor()

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
        # instantiate cursor for connection
        cursor = connection.cursor()

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
            print("%d) Type: %s\n" % (i + 1, preferred_type))


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
        # instantiate cursor for connection
        cursor = connection.cursor()

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
        # instantiate cursor for connection
        cursor = connection.cursor()

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
        # instantiate cursor for connection
        cursor = connection.cursor()

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
    if (cc_type.upper() != "VISA" and cc_type.upper() != "AMERICAN EXPRESS" and cc_type.upper() != "MASTERCARD"):
        print("* Credit card type: Must be Visa, American Express, or Mastercard")
        input_error = True

    return input_error

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
        # instantiate cursor for connection
        cursor = connection.cursor()

        # add new payment info to database and associate with user
        cursor.callproc("user_adds_payment_info", [current_user, cc_number, expiration_date, cc_type, ])

        # commit updated data
        connection.commit()

        # update success and show new updated values
        print("\nPayment info successfully added!\n")
        user_info(current_user)

    except pymysql.Error as e:
        # catch any errors produced by mysql
        print('Error: %d: %s' % (e.args[0], e.args[1]))


def delete_payment_info(current_user):
    # Get credit card info from user
    print("\n-- Delete Payment Info --")
    cc_number = input("Enter the credit card # you would like to delete: ")

    try:
        # instantiate cursor for connection
        cursor = connection.cursor()

        # delete user association with payment info from database
        cursor.callproc("user_deletes_payment_info", [current_user, cc_number, ])

        # commit updated data
        connection.commit()

        # update success and show new updated values
        print("\nPayment info successfully deleted!\n")
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
            # TODO: Add new payment preference
            print("ADD PAYMENT PREFERENCE")

        elif (selection == "7"):
            # TODO: Delete payment preference
            print("DELETE PAYMENT PREFERENCE")

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



# Menu options for home page after log in
def display_menu_options():
    print("\n-- Community Rentals Home --")
    print("What would you like to do?")
    print("1. Profile\n2. Manage listings\n3. Log out")


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
            # TODO: navigate to manage listings page
            print("\nMANAGE LISTINGS PAGE")

        elif (selection == "3"):
            # TODO: logout - navigate back to login screen or quit?
            logout = True

        else:
            # Invalid selection - prompt user to choose again
            print("Invalid option. Please choose a number that corresponds to a menu option.")

    return



def start_community_rentals_app():
    # welcome message
    print("\nWelcome to the Community Rentals App!")

    # prompt user to login or signup
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

    # begin Community Rentals App
    print("\nDirecting you to the Community Rentals Application...")
    start_community_rentals_app()

    # close connection
    connection.close()
