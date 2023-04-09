import pymysql

# username = input("Enter your MySQL username: ")
# username = username.strip()
# password = input("Enter your MySQL password: ")
# password = password.strip()

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='',
                             database='community_rentals',
                             cursorclass=pymysql.cursors.DictCursor)


cur = connection.cursor()
stmt_select = "call all_users()"
cur.execute(stmt_select)
users = cur.fetchall()
users_list = [d['username'] for d in users]
for user in users_list:
    print("  " + user)

user = input("Select a user from those listed above: ")
user = user.strip()
while user not in users_list:
    print("ERROR: Selected user is invalid")
    user = input("Select a user from those listed above: ")

stmt_procedure = "call search_items_by_seller('" + user + "')"
cur.execute(stmt_procedure)
results = cur.fetchall()
for result in results:
    print(result)

connection.close()