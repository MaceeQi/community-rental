# Community Rental Database
Final project for CS5200
By Chanon Bovornvirakit and Macee Qi

## Description
For our final project, we created a community rental application. The data stored will contain users, items, item categories, item listings, user wishlists, ratings for users and items, and payment information. The users of the application can be a customer and/or a seller. A customer can rent items from sellers and create a wishlist of items they would like to rent. A seller owns items that customers can rent and list items they have available. Items for rent belong to a specific category (e.g., bike, book, sports equipment, etc.). Customers and sellers can rate each other, based on how well they treated the item while in use (customer), and how communicative they were (seller). Customers can also leave a rating for items they have rented. Users can search for items (by category, owner, or item ID) that they’re looking for. The database also keeps track of the different payment information and payment types for each user. 

## Getting Started
### Steps to run application for the first time:
- python3 -m pip install PyMySQL
- pip install cryptography
- pip install bcrypt
- pip install tabulate
- python3 community_rental.py

### Steps to run application after the first time:
- python3 community_rental.py
