import pymysql
import tabulate


# print table (tabulate):
def print_table(rows, keys):
    print(tabulate.tabulate(rows, keys, tablefmt='grid'))


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
        print("\n-- All Users --")
        print_table(rows, desired_keys)
        return users

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


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
        print("\n-- All Sellers --")
        print_table(rows, desired_keys)
        return sellers

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


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
        print("\n-- All Customers --")
        print_table(rows, desired_keys)
        return customers

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# list all items
def all_items():
    try:
        cursor.callproc('all_items')
        items = cursor.fetchall()
        desired_keys = ['id', 'owner', 'description', 'category', 'average_rating']
        rows = []
        for item in items:
            rows.append([item.get(k) for k in desired_keys])
        print("\n-- All items --")
        print_table(rows, desired_keys)
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
        print("\n-- All Categories --")
        print_table(rows, desired_keys)
        return categories

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
        print("\n-- All Rentals --")
        print_table(rows, desired_keys)
        return rentals

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# search for user by username/firstname/lastname
def search_user(name):
    try:
        cursor.callproc('search_user', [name])
        users = cursor.fetchall()
        desired_keys = ['username', 'first_name', 'last_name', 'phone', 'average_rating',
                        'street_number', 'street_name', 'city', 'state', 'zipcode']
        rows = []
        for user in users:
            rows.append([user.get(k) for k in desired_keys])
        print("\n-- Users found matching the name '" + name + "' --")
        print_table(rows, desired_keys)
        return users

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# search for item by category
def search_items_by_category(category):
    try:
        cursor.callproc('search_items_by_category', [category])
        items = cursor.fetchall()
        desired_keys = ['id', 'owner', 'description', 'category', 'average_rating']
        rows = []
        for item in items:
            rows.append([item.get(k) for k in desired_keys])
        print("\n-- Items found matching the '" + category + "' category --")
        print_table(rows, desired_keys)
        return items

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# search for item by category
def search_item_by_id(item_id):
    try:
        cursor.callproc('search_item_by_id', [item_id])
        items = cursor.fetchall()
        desired_keys = ['id', 'owner', 'description', 'category', 'average_rating']
        rows = []
        for item in items:
            rows.append([item.get(k) for k in desired_keys])
        print("\n-- Searching for item with ID '" + item_id + "' --")
        print_table(rows, desired_keys)
        return items

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


def search_items_by_seller(seller):
    try:
        cursor.callproc('search_items_by_seller', [seller])
        items = cursor.fetchall()
        desired_keys = ['id', 'owner', 'description', 'category', 'average_rating']
        rows = []
        for item in items:
            rows.append([item.get(k) for k in desired_keys])
        print("\n-- Items owned by '" + seller + "' --")
        print_table(rows, desired_keys)
        return items

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


def search_listings(username):
    try:
        cursor.callproc('get_user_listings', [username])
        listings = cursor.fetchall()
        desired_keys = ['item', 'owner', 'description', 'category', 'average_rating']
        rows = []
        for listing in listings:
            rows.append([listing.get(k) for k in desired_keys])
        print("\n-- All listings by '" + username + "' --")
        print_table(rows, desired_keys)
        return listings

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# look up a wishlist
def get_wishlist(customer):
    try:
        cursor.callproc('list_wishlist', [customer])
        wishlist = cursor.fetchall()
        desired_keys = ['item', 'description', 'category']
        rows = []
        for item in wishlist:
            rows.append([item.get(k) for k in desired_keys])
        print("\n-- All items on '" + customer + "''s wishlist --")
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
        item = input("Which item would you like to add to your wishlist?    ")
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
        item = input("Which item would you like to delete from your wishlist?    ")
        cursor.callproc('delete_wishlist_item', [customer, item])
        get_wishlist(customer)
        return

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# rate user
def rate_user(current):
    try:
        print("\n-- Rating a user --")
        all_users()
        username = input("Which user (username) would you like to rate?    ")
        rating = input("What would you rate this user from 1-5?    ")
        cursor.callproc('rate_user', [current, username, rating])
        search_user(username)
        return

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# rate item
def rate_item(current):
    try:
        print("\n-- Rating an item --")
        all_items()
        item = input("Which item would you like to rate?    ")
        rating = input("What would you rate this item from 1-5?    ")
        cursor.callproc('rate_item', [current, item, rating])
        search_item_by_id(item)

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
        print("\n-- Your current payment info --")
        print_table(rows, desired_keys)

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


# rent an item
def rent_item(current):
    try:
        print("\n-- Renting an item --")
        all_listings()
        item = input("Which item would you like to rent?    ")
        get_user_payment(current)
        payment = input("Which payment method would you use?    ")
        rental_date = input("When are you renting this item? (YYYY-MM-DD)    ")
        return_date = input("When are you returning this item? (YYYY-MM-DD)   ")
        cursor.callproc('rent_item', [item, current, payment, rental_date, return_date])
        all_rentals()

    except pymysql.Error as e:
        print('Error: %d: %s' % (e.args[0], e.args[1]))


def switch(command, current):
    if command == "A":
        return all_users()
    elif command == "S":
        return all_sellers()
    elif command == "C":
        return all_customers()
    elif command == "I":
        return all_items()
    elif command == "L":
        return all_listings()
    elif command == "R":
        return all_rentals()
    elif command == "Search":
        print("What would you like to search for?\n"
              " U: Users\n"
              " I: Items\n"
              " L: Listings\n"
              " W: Wishlist")
        search = input("Enter search target: ")
        search = search.strip()
        search = search.capitalize()
        if search == "U":
            name = input("Who would you like to search for?     ")
            search_user(name)
        elif search == "I":
            all_item_categories()
            category = input("What item category would you like to search for?     ")
            search_items_by_category(category)
        elif search == "L":
            all_users()
            username = input("Whose listings would you like to search for?     ")
            search_listings(username)
        elif search == "W":
            all_customers()
            customer = input("Whose wishlist would you like to search for?     ")
            get_wishlist(customer)
        else:
            print("Error: Invalid input")
    elif command == "Write":
        print("What would you like to do?\n"
              " W: Update wishlist\n"
              " I: Rate an item\n"
              " U: Rate a user\n"
              " R: Rent an item")
        write = input("Enter write target: ")
        write = write.strip()
        write = write.capitalize()
        if write == "W":
            get_wishlist(current)
            choice = input("Would you like to add or a delete an item?\n"
                           " A: Add\n"
                           " D: Delete\n")
            choice = choice.strip()
            choice = choice.capitalize()
            if choice == "A":
                add_wishlist(current)
            elif choice == "D":
                delete_wishlist(current)
        elif write == "I":
            rate_item(current)
        elif write == "U":
            rate_user(current)
        elif write == "R":
            rent_item(current)
        else:
            print("Error: Invalid input")
    else:
        print("Error: Invalid command")


if __name__ == "__main__":
    sql_username = input("Enter your MySQL username: ")
    sql_username = sql_username.strip()
    sql_password = input("Enter your MySQL password: ")
    sql_password = sql_password.strip()

    connection = pymysql.connect(host='localhost',
                                 user=sql_username,
                                 password=sql_password,
                                 database='community_rentals',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor = connection.cursor()
    current_user = 'cb123'
    while True:
        print("\nCommands implemented so far:\n"
              " Q: Quit\n"
              " A: all users\n"
              " S: all sellers\n"
              " C: all customers\n"
              " I: all items\n"
              " L: all listings\n"
              " R: all rentals\n"
              " Search: search for something/someone\n"
              " Write: add/update/delete something in the database")
        command = input("\nEnter a command: ")
        command = command.strip()
        command = command.capitalize()
        if command == "Q":
            break
        ret = switch(command, current_user)

    connection.close()
