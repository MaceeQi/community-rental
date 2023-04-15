import pymysql
import tabulate

# username = input("Enter your MySQL username: ")
# username = username.strip()
# password = input("Enter your MySQL password: ")
# password = password.strip()


# list all users
def all_users(cur):
    stmt = "call all_users()"
    cur.execute(stmt)
    users = cur.fetchall()
    desired_keys = ['username', 'first_name', 'last_name', 'phone', 'average_rating',
              'street_number', 'street_name', 'city', 'state', 'zipcode']
    rows = []
    for user in users:
        rows.append([user.get(k) for k in desired_keys])
    print(tabulate.tabulate(rows, desired_keys))
    return users


# list all sellers
def all_sellers(cur):
    stmt = "call all_sellers()"
    cur.execute(stmt)
    sellers = cur.fetchall()
    desired_keys = ['username', 'first_name', 'last_name', 'phone', 'average_rating',
                    'street_number', 'street_name', 'city', 'state', 'zipcode']
    rows = []
    for seller in sellers:
        rows.append([seller.get(k) for k in desired_keys])
    print(tabulate.tabulate(rows, desired_keys))
    return sellers


# list all customers
def all_customers(cur):
    stmt = "call all_customers()"
    cur.execute(stmt)
    customers = cur.fetchall()
    desired_keys = ['username', 'first_name', 'last_name', 'phone', 'average_rating',
                    'street_number', 'street_name', 'city', 'state', 'zipcode']
    rows = []
    for customer in customers:
        rows.append([customer.get(k) for k in desired_keys])
    print(tabulate.tabulate(rows, desired_keys))
    return customers


# list all items
def all_items(cur):
    stmt = "call all_items()"
    cur.execute(stmt)
    items = cur.fetchall()
    desired_keys = ['id', 'owner', 'description', 'category', 'average_rating']
    rows = []
    for item in items:
        rows.append([item.get(k) for k in desired_keys])
    print(tabulate.tabulate(rows, desired_keys))
    return items


# list all listings
def all_listings(cur):
    stmt = "call all_listings()"
    cur.execute(stmt)
    listings = cur.fetchall()
    desired_keys = ['item', 'owner', 'description', 'category', 'average_rating',
                    'price', 'quantity']
    rows = []
    for listing in listings:
        rows.append([listing.get(k) for k in desired_keys])
    print(tabulate.tabulate(rows, desired_keys))
    return listings


# list all rentals
def all_rentals(cur):
    stmt = "call all_rentals()"
    cur.execute(stmt)
    rentals = cur.fetchall()
    desired_keys = ['item', 'owner', 'customer', 'description', 'category',
                    'average_rating', 'rental_date', 'return_date']
    rows = []
    for rental in rentals:
        rows.append([rental.get(k) for k in desired_keys])
    print(tabulate.tabulate(rows, desired_keys))
    return rentals


# search for user by username/firstname/lastname
def search_user(cur, name):
    stmt = "call search_user('" + name + "')"
    cur.execute(stmt)
    users = cur.fetchall()
    desired_keys = ['username', 'first_name', 'last_name', 'phone', 'average_rating',
                    'street_number', 'street_name', 'city', 'state', 'zipcode']
    rows = []
    for user in users:
        rows.append([user.get(k) for k in desired_keys])
    print("\nUsers found matching the name '" + name + "':")
    print(tabulate.tabulate(rows, desired_keys))
    return users


# search for item by category
def search_category(cur, category):
    stmt = "call search_items_by_category('" + category + "')"
    cur.execute(stmt)
    items = cur.fetchall()
    desired_keys = ['id', 'owner', 'description', 'category', 'average_rating']
    rows = []
    for item in items:
        rows.append([item.get(k) for k in desired_keys])
    print("\nitems found matching the '" + category + "' category:")
    print(tabulate.tabulate(rows, desired_keys))
    return items


# rate user
def rate_user(cur, username, rating):
    return 0


# rate item
def rate_item(cur, item, rating):
    return 0


def switch(cur, command):
    if command == "A":
        return all_users(cur)
    elif command == "S":
        return all_sellers(cur)
    elif command == "C":
        return all_customers(cur)
    elif command == "I":
        return all_items(cur)
    elif command == "L":
        return all_listings(cur)
    elif command == "R":
        return all_rentals(cur)
    elif command == "Search":
        print("What would you like to search for?\n"
              " U: Users\n"
              " I: Items")
        search = input("Enter search target: ")
        search = search.strip()
        search = search.capitalize()
        if search == "U":
            name = input("Who would you like to search for?     ")
            search_user(cur, name)
        elif search == "I":
            category = input("What item category would you like to search for?     ")
            search_category(cur, category)

    else:
        print("Error: Command not detected")


def main():
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='',
                                 database='community_rentals',
                                 cursorclass=pymysql.cursors.DictCursor)


    cur = connection.cursor()
    while True:
        print("\nCommands implemented so far:\n"
              " Q: Quit\n"
              " A: all users\n"
              " S: all sellers\n"
              " C: all customers\n"
              " I: all items\n"
              " L: all listings\n"
              " R: all rentals\n"
              " Search: search for something/someone")
        command = input("\nEnter a command: ")
        command = command.strip()
        command = command.capitalize()
        if command == "Q":
            break
        ret = switch(cur, command)

    # user = input("Select a user from those listed above: ")
    # user = user.strip()
    # while user not in users_list:
    #     print("ERROR: Selected user is invalid")
    #     user = input("Select a user from those listed above: ")
    #
    # stmt_procedure = "call search_items_by_seller('" + user + "')"
    # cur.execute(stmt_procedure)
    # results = cur.fetchall()
    # for result in results:
    #     print(result)

    connection.close()


if __name__ == "__main__":
    main()