USE community_rentals;

-- Database programming objects for users and listings


-- login
-- error if username doesn't exist
-- error if username exists, password doesn't match


-- signup
-- error if username already exists
-- insert new user to user table
-- trigger (before insert on user table): creates address in address table if doesn't exist


-- update user info
-- update name
-- update phone 
-- update user type
-- update address
-- trigger (before update on user): create new address in address table ? (or does ON UPDATE CASCADE handle this)


-- add payment info
-- insert new user/payment_info to user_payment table
-- trigger (before insert on user_payment): insert new payment into payment_info if doesn't exist
-- trigger (before insert on payment_info): insert new payment type into payment_type if doesn't exist


-- delete payment info


-- add payment preference
-- error if user isn't seller 
-- insert new payment preference for seller
-- trigger (before insert on payment_preference): insert new payment type into payment_type if doesn't exist


-- create new listing
-- error if user isn't seller 
-- insert new listing to listing table
-- trigger (before insert on listing): insert new item to item table if doesn't exist


-- update listing
-- update price from listing table
-- update quantity from listing table


-- update item
-- update item description from item table


-- delete listing
-- delete listing from listing table