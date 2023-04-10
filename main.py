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


def hash_password(password):
    # add salt to password
    salt = bcrypt.gensalt()

    # hash the password
    hashed_password = bcrypt.hashpw(password, salt)

    return hashed_password


def login(connection):
    print("Login")
    return True

def signup(connection):
    print("Signup")
    return True

def prompt_login_signup(connection):
    successful_login = False

    # continue prompting user to login or signup
    while (not successful_login):
        print("\nWould you like to:\n1. Login\n2. Sign Up")
        choice = input("Please select an option: ")

        # convert choice to all lowercase
        choice = choice.lower()

        # allow user to choose by number or by word
        if (choice == "1" or choice == "login"):
            successful_login = login(connection)
        elif (choice == "2" or choice == "sign up"):
            successful_login = signup(connection)
        else:
            print("Invalid option. Please enter '1' or 'Login' to login, '2' or 'Sign Up' to sign up.")


    return

def start_community_rentals_app(connection):
    # welcome message
    print("\nWelcome to the Community Rentals App!")

    # prompt user to login or signup
    prompt_login_signup(connection)



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
