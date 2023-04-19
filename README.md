# Community Rental
Developed as a final project for CS5200 - Database Management Systems

## Description
This is an e-commerce rental platform that facilitates item rentals within a community. 

The database stores users (customer/seller), addresses, payment information, payment types, seller payment preferences, items, item categories, wishlists, listings, and rentals.

Users of the application are all customers, but they can also be a seller if they have an item listed for rent. Each user can save their credit card payment information and sellers can specify which credit card types they prefer. A customer can rent items that are listed by sellers and create a wishlist of items they would like to rent. A seller owns items that customers can rent and list items they have available. 

Items for rent belong to a specified category (e.g. books, sports equipment, clothing, etc.). Users can rate each other on a scale of 1-5, based on how well a customer treated the item while in use, or how communicative a seller was. Users can also rate items they have rented. Users can search for items (by category, owner, or item ID) or search for other users within the database.

Currently, this release only supports command-line interaction.

## Getting Started
### Steps to run application for the first time:
- Run project_data_dump.sql
- python3 -m pip install PyMySQL
- pip install cryptography
- pip install bcrypt
- pip install tabulate
- python3 community_rental.py

### Steps to run application after the first time:
- python3 community_rental.py

## Technical Specifications
We used SQL and MySQL Workbench to create and manage the relational database. The user application was created with Python 3.9 and connected to the database via PyMySQL. We used 'bcrypt' and 'cryptography' Python packages to encrypt user passwords, and 'tabulate' Python package to improve the command-line table presentation.

- Bcrypt: https://pypi.org/project/bcrypt/ 
- Cryptography: https://pypi.org/project/cryptography/
- Tabulate: https://pypi.org/project/tabulate/

## Authors
- Chanon Bovornvirakit
- Macee Qi
