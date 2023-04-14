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
    exit = False
    next_steps = ""

    while (not exit):
        next_steps = input("\nWould you liked to try again (y/n)? ").lower()

        if (next_steps == "n" or next_steps == "y"):
            exit = True
        else:
            print("Please enter a valid input: 'y' or 'n'")

    return next_steps

# login function
def login(connection):
    print("\nLogin")

    # prompt user to enter login credentials
    exit = False
    while (not exit):
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
                    exit = True
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

# Validate user input for signing up
def validate_signup_user_input(phone, street_num, state, zipcode):
    input_error = False
    if (not phone.isnumeric() or len(phone) > 11):
        print("* Phone number: Must be all numbers and cannot be longer than 11 digits")
        input_error = True

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


# sign up function
def signup(connection):
    print("\nSign Up")

    # prompt user for info needed for creating a new user
    exit = False
    while (not exit):
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
                exit = True
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
                exit = True
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

def quit_program(connection):
    print("\nExiting...\nGoodbye!\n")
    connection.close()
    quit()

# Prompt user to sign up or login
def prompt_login_signup(connection):
    successful_login = False
    current_user = None

    # continue prompting user to login or signup
    while (not successful_login):
        print("\nWould you like to:\n1. Login\n2. Sign Up\n3. Quit")
        choice = input("Please select an option: ")

        # convert choice to all lowercase
        choice = choice.lower()

        # allow user to choose by number or by word
        if (choice == "1" or choice == "login"):
            # navigate to login page
            successful_login, current_user = login(connection)

        elif (choice == "2" or choice == "sign up"):
            # navigate to sign up page
            signup(connection)

        elif (choice == "3" or choice == "quit"):
            # quit program
            quit_program(connection)

        else:
            print("Invalid option. Please enter '1' or 'Login' to login, '2' or 'Sign Up' to sign up, "
                  "'3' or 'Quit' to exit.")

    return successful_login, current_user

def display_menu():
    print("\nWhat would you like to do?")
    print("1. Profile\n2. Manage listings\n3. Logout")

def home_menu(connection, current_user):
    logout = False

    # menu of options
    while (not logout):
        display_menu()
        selection = input("Choose an option #: ")

        if (selection == "1"):
            # TODO: navigate to profile page
            print("\nPROFILE PAGE")

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



def start_community_rentals_app(connection):
    # welcome message
    print("\nWelcome to the Community Rentals App!")

    # prompt user to login or signup
    successful_login, current_user = prompt_login_signup(connection)

    # navigate to home page if login successful
    if (successful_login and current_user != None):
        print("\nWelcome, " + current_user + "!")
        home_menu(connection, current_user)

    # exit program
    quit_program(connection)


if __name__ == '__main__':
    database = "community_rentals"
    connection = None

    # prompt user for valid username/password to connect to database
    print("\nPlease enter your MySQL username and password to access the database.")
    while (connection == None):
        connection = connect_to_database(database)

    # begin Community Rentals App
    print("\nDirecting you to the Community Rentals Application...")
    start_community_rentals_app(connection)

    # close connection
    connection.close()
