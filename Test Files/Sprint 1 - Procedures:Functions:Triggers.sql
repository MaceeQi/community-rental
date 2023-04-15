USE community_rentals;

-- Basic SELECT Procedures:
-- Search for all addresses
DROP PROCEDURE IF EXISTS all_addresses;
DELIMITER $$
CREATE PROCEDURE all_addresses()
BEGIN
	SELECT * FROM address;
END$$
DELIMITER ;

-- Search for all items
DROP PROCEDURE IF EXISTS all_items;
DELIMITER $$
CREATE PROCEDURE all_items()
BEGIN
	SELECT * FROM item;
END$$
DELIMITER ;

-- Search for all items in a category
DROP PROCEDURE IF EXISTS search_items;
DELIMITER $$
CREATE PROCEDURE search_items(category_p VARCHAR(50))
BEGIN
	SELECT * FROM item WHERE category = category_p;
END$$
DELIMITER ;

-- Search for all listings
DROP PROCEDURE IF EXISTS all_listings;
DELIMITER $$
CREATE PROCEDURE all_listings()
BEGIN
	SELECT * FROM item JOIN listing ON item.id = listing.item;
END$$
DELIMITER ;

-- Search for all listings by seller
DROP PROCEDURE IF EXISTS seller_listings;
DELIMITER $$
CREATE PROCEDURE seller_listings(seller_p VARCHAR(64))
BEGIN
	SELECT * FROM item JOIN listing ON item.id = listing.item WHERE seller = seller_p;
END$$
DELIMITER ;

-- Search for all rentals
DROP PROCEDURE IF EXISTS all_rentals;
DELIMITER $$
CREATE PROCEDURE all_rentals()
BEGIN
	SELECT * FROM item JOIN rental ON item.id = rental.item;
END$$
DELIMITER ;


-- Search for all users
DROP PROCEDURE IF EXISTS all_users;
DELIMITER $$
CREATE PROCEDURE all_users()
BEGIN
	SELECT * FROM user;
END$$
DELIMITER ;

-- Search for all customers
DROP PROCEDURE IF EXISTS all_customers;
DELIMITER $$
CREATE PROCEDURE all_customers()
BEGIN
	SELECT * FROM user WHERE is_customer = true;
END$$
DELIMITER ;

-- Search for all sellers
DROP PROCEDURE IF EXISTS all_sellers;
DELIMITER $$
CREATE PROCEDURE all_sellers()
BEGIN
	SELECT * FROM user WHERE is_seller = true;
END$$
DELIMITER ;

-- Search for all payment info
DROP PROCEDURE IF EXISTS all_payment_info;
DELIMITER $$
CREATE PROCEDURE all_payment_info()
BEGIN
	SELECT * FROM payment_info;
END$$
DELIMITER ;

-- Search for all user_payment
DROP PROCEDURE IF EXISTS all_user_payment;
DELIMITER $$
CREATE PROCEDURE all_user_payment()
BEGIN
	SELECT * FROM user_payment JOIN payment_info ON user_payment.payment_info = payment_info.cc_number;
END$$
DELIMITER ;

-- Search for user by username/firstname/lastname
DROP PROCEDURE IF EXISTS search_user;
DELIMITER $$
CREATE PROCEDURE search_user(name_p VARCHAR(64))
BEGIN
	SELECT * FROM user HAVING username = name_p OR first_name = name_p OR last_name = name_p;
END$$
DELIMITER ;

-- Get all items in a specified customer's wishlist
DROP PROCEDURE IF EXISTS list_wishlist;
DELIMITER $$
CREATE PROCEDURE list_wishlist(customer_p VARCHAR(64))
BEGIN
	SELECT * FROM item JOIN wishlist ON item.id = wishlist.item
    WHERE customer = customer_p;
END$$
DELIMITER ;


-- Helper Functions:
-- Returns TRUE if specified user is a customer, FALSE otherwise
DROP FUNCTION IF EXISTS user_is_customer;
DELIMITER $$
CREATE FUNCTION user_is_customer(user_p VARCHAR(64))
RETURNS BOOL DETERMINISTIC READS SQL DATA
BEGIN
	DECLARE customer BOOL DEFAULT TRUE;
    SELECT is_customer INTO customer FROM user WHERE username = user_p;
    RETURN (customer);
END$$
DELIMITER ;

-- Returns TRUE if specified user is a seller, FALSE otherwise
DROP FUNCTION IF EXISTS user_is_seller;
DELIMITER $$
CREATE FUNCTION user_is_seller(user_p VARCHAR(64))
RETURNS BOOL DETERMINISTIC READS SQL DATA
BEGIN
	DECLARE seller BOOL DEFAULT FALSE;
    SELECT is_seller INTO seller FROM user WHERE username = user_p;
    RETURN (seller);
END$$
DELIMITER ;

-- Returns TRUE if specified item is listed for rent FALSE otherwise
DROP FUNCTION IF EXISTS item_in_listing;
DELIMITER $$
CREATE FUNCTION item_in_listing(item_p INT)
RETURNS BOOL DETERMINISTIC READS SQL DATA
BEGIN
	DECLARE item_exists BOOL DEFAULT FALSE;
    IF (item_p IN (SELECT item FROM listing)) THEN
		SET item_exists = TRUE;
	END IF;
    RETURN (item_exists);
END$$
DELIMITER ;

-- Returns TRUE if specified cc_number exists, FALSE otherwise
DROP FUNCTION IF EXISTS payment_info_exists;
DELIMITER $$
CREATE FUNCTION payment_info_exists(cc_number_p VARCHAR(16))
RETURNS BOOL DETERMINISTIC READS SQL DATA
BEGIN
	DECLARE payment_exists BOOL DEFAULT FALSE;
    IF (cc_number_p IN (SELECT cc_number FROM payment_info WHERE cc_number = cc_number_p)) THEN
		SET payment_exists = TRUE;
	END IF;
    RETURN (payment_exists);
END$$
DELIMITER ;

-- Returns TRUE if specified payment method is associated with the specified user, FALSE otherwise
DROP FUNCTION IF EXISTS user_payment_exists;
DELIMITER $$
CREATE FUNCTION user_payment_exists(user_p VARCHAR(64), payment_p VARCHAR(16))
RETURNS BOOL DETERMINISTIC READS SQL DATA
BEGIN
	DECLARE payment_exists BOOL DEFAULT FALSE;
    IF (payment_p IN (SELECT payment_info FROM user_payment WHERE user = user_p)) THEN
		SET payment_exists = TRUE;
	END IF;
    RETURN (payment_exists);
END$$
DELIMITER ;

-- Returns the quantity of the specified item listed for rent
DROP FUNCTION IF EXISTS num_item_listed;
DELIMITER $$
CREATE FUNCTION num_item_listed(item_p INT)
RETURNS INT DETERMINISTIC READS SQL DATA
BEGIN
	DECLARE item_quantity INT DEFAULT 0;
    SELECT quantity INTO item_quantity FROM listing WHERE item = item_p;
	RETURN (item_quantity);
END$$
DELIMITER ;

-- Returns the number of items seller has listed
DROP FUNCTION IF EXISTS seller_listing_count;
DELIMITER $$
CREATE FUNCTION seller_listing_count(seller_p VARCHAR(64))
RETURNS INT DETERMINISTIC READS SQL DATA
BEGIN
	DECLARE listing_count INT DEFAULT 0;
    SELECT COUNT(*) INTO listing_count FROM listing WHERE seller = seller_p;
	RETURN (listing_count);
END$$
DELIMITER ;



-- INSERTs/DELETEs:
-- Rent item:
DROP PROCEDURE IF EXISTS rent_item;
DELIMITER $$
CREATE PROCEDURE rent_item(item_p INT, renter_p VARCHAR(64), payment_p VARCHAR(16), rent_date DATE, return_date DATE)
BEGIN
	IF NOT (user_is_customer(renter_p)) THEN
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = 'User is not a customer';
    ELSEIF NOT (item_in_listing(item_p)) THEN
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = 'Item not found in listings';
	ELSEIF NOT (user_payment_exists(renter_p, payment_p)) THEN
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = 'Given payment not associated with user';
    ELSEIF (DATE(rent_date) > DATE(return_date)) THEN
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = 'Return date must be after rent date';
	ELSE
		INSERT INTO rental VALUES (item_p, renter_p, payment_p, rent_date, return_date);
        UPDATE listing SET quantity = quantity - 1 WHERE item = item_p;
        IF (num_item_listed(item_p) <= 0) THEN
			DELETE FROM listing WHERE item = item_p;
        END IF;
    END IF;
END$$
DELIMITER ;


-- Rate item
DROP PROCEDURE IF EXISTS rate_item;
DELIMITER $$
CREATE PROCEDURE rate_item(item_p INT, rating_p INT)
BEGIN
	IF (rating_p > 5 OR rating_p < 1) THEN
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = 'Ratings must be between 1 and 5';
	ELSE
		UPDATE item SET total_rating = total_rating + rating_p WHERE id = item_p;
        UPDATE item SET rating_count = rating_count + 1 WHERE id = item_p;
        UPDATE item SET average_rating = total_rating / rating_count WHERE id = item_p;
    END IF;
END$$
DELIMITER ;

-- Rate user
DROP PROCEDURE IF EXISTS rate_user;
DELIMITER $$
CREATE PROCEDURE rate_user(customer_p VARCHAR(64), rating_p INT)
BEGIN
	IF (rating_p > 5 OR rating_p < 1) THEN
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = 'Ratings must be between 1 and 5';
	ELSE
		UPDATE user SET total_rating = total_rating + rating_p WHERE username = customer_p;
        UPDATE user SET rating_count = rating_count + 1 WHERE username = customer_p;
        UPDATE user SET average_rating = total_rating / rating_count WHERE username = customer_p;
    END IF;
END$$
DELIMITER ;

-- Add item to wishlist
DROP PROCEDURE IF EXISTS wish_for_item;
DELIMITER $$
CREATE PROCEDURE wish_for_item(customer_p VARCHAR(64), item_p INT)
BEGIN
	IF NOT EXISTS (SELECT * FROM user WHERE username = customer_p) THEN
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = 'User does not exist';
	ELSEIF (user_is_customer(customer_p) = FALSE) THEN
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = 'User is not a customer';
	ELSEIF NOT EXISTS (SELECT * FROM item WHERE id = item_p) THEN
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = 'Item does not exist';
	ELSEIF EXISTS (SELECT * FROM wishlist WHERE customer = customer_p AND item = item_p) THEN
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = 'Item already wished for';
	ELSE
		INSERT INTO wishlist VALUES (item_p, customer_p);
    END IF;
END$$
DELIMITER ;

-- Delete item from wishlist
DROP PROCEDURE IF EXISTS delete_wishlist_item;
DELIMITER $$
CREATE PROCEDURE delete_wishlist_item(customer_p VARCHAR(64), item_p INT)
BEGIN
    IF NOT EXISTS (SELECT * FROM wishlist WHERE customer = customer_p AND item = item_p) THEN
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = 'Entry does not exist in wishlist';
	ELSE
        DELETE FROM wishlist WHERE customer = customer_p AND item = item_p;
    END IF;
END$$
DELIMITER ;

-- Add payment info
DROP PROCEDURE IF EXISTS add_payment_info;
DELIMITER $$
CREATE PROCEDURE add_payment_info(cc_number_p VARCHAR(16), expiration_date_p DATE, type_p ENUM('VISA', 'AMERICAN EXPRESS', 'MASTERCARD'))
BEGIN
	IF (payment_info_exists(cc_number_p)) THEN
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = 'Payment info already exists';
	ELSE
		INSERT INTO payment_info VALUES (cc_number_p, expiration_date_p, type_p);
    END IF;
END$$
DELIMITER ;

-- Delete payment info
DROP PROCEDURE IF EXISTS del_payment_info;
DELIMITER $$
CREATE PROCEDURE del_payment_info(cc_number_p VARCHAR(16))
BEGIN
	IF NOT (payment_info_exists(cc_number_p)) THEN
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = 'Payment info does not exists';
	ELSE
		DELETE FROM payment_info WHERE cc_number = cc_number_p;
    END IF;
END$$
DELIMITER ;

-- Add user_payment
DROP PROCEDURE IF EXISTS add_user_payment;
DELIMITER $$
CREATE PROCEDURE add_user_payment(username_p VARCHAR(64), payment_p VARCHAR(16))
BEGIN
	IF (user_payment_exists(username_p, payment_p)) THEN
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = 'Payment already associated with user';
	ELSEIF NOT (payment_info_exists(payment_p)) THEN
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = 'Payment info does not exist';
	ELSE
		INSERT INTO user_payment VALUES (username_p, payment_p);
    END IF;
END$$
DELIMITER ;

-- Delete user_payment
DROP PROCEDURE IF EXISTS del_user_payment;
DELIMITER $$
CREATE PROCEDURE del_user_payment(username_p VARCHAR(64), payment_p VARCHAR(16))
BEGIN
	IF NOT (user_payment_exists(username_p, payment_p)) THEN
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = 'Payment not associated with user';
	ELSE
		DELETE FROM user_payment WHERE user = username_p AND payment_info = payment_p;
    END IF;
END$$
DELIMITER ;


-- UPDATEs:
-- Change user's is_seller status
DROP PROCEDURE IF EXISTS update_user_seller;
DELIMITER $$
CREATE PROCEDURE update_user_seller(username_p VARCHAR(64), status_p BOOL)
BEGIN
	IF NOT (status_p) AND (user_is_seller(username_p)) AND (seller_listing_count(username_p) > 0) THEN
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = 'is_seller cannot be false while user has items listed for rent';
	ELSE
		UPDATE user SET is_seller = status_p WHERE username = username_p;
	END IF;
END$$
DELIMITER ;

-- Change user's is_customer status
DROP PROCEDURE IF EXISTS update_user_customer;
DELIMITER $$
CREATE PROCEDURE update_user_customer(username_p VARCHAR(64), status_p BOOL)
BEGIN
	UPDATE user SET is_customer = status_p WHERE username = username_p;
END$$
DELIMITER ;

-- Change user's first name
DROP PROCEDURE IF EXISTS update_user_first_name;
DELIMITER $$
CREATE PROCEDURE update_user_first_name(username_p VARCHAR(64), first_name_p VARCHAR(50))
BEGIN
	UPDATE user SET first_name = first_name_p WHERE username = username_p;
END$$
DELIMITER ;

-- Change user's last name
DROP PROCEDURE IF EXISTS update_user_last_name;
DELIMITER $$
CREATE PROCEDURE update_user_last_name(username_p VARCHAR(64), last_name_p VARCHAR(50))
BEGIN
	UPDATE user SET last_name = last_name_p WHERE username = username_p;
END$$
DELIMITER ;

-- Change user's address
/* not currently working, can't update composite foreign key
DROP PROCEDURE IF EXISTS update_user_address;
DELIMITER $$
CREATE PROCEDURE update_user_address(username_p VARCHAR(64), number_p INT, street_p VARCHAR(50), 
										city_p VARCHAR(50), state_p CHAR(2), zipcode_p CHAR(5))
BEGIN
	IF NOT EXISTS(SELECT * FROM address WHERE address.number = number_p AND address.street = street_p
										AND address.city = city_p AND address.state = state_p
										AND address.zipcode = city_p) THEN
		INSERT INTO address VALUES (number_p, street_p, city_p, state_p, zipcode_p);
    END IF;
	UPDATE user SET street_number = number_p WHERE username = username_p;
	UPDATE user SET street_name = street_p WHERE username = username_p;
	UPDATE user SET city = city_p WHERE username = username_p;
	UPDATE user SET state = state_p WHERE username = username_p;
	UPDATE user SET zipcode = zipcode_p WHERE username = username_p;
END$$
DELIMITER ;
*/


-- Triggers:
/* rating triggers not currently working
-- Trigger: change rating_count by 1 and recalculate average rating when total rating changes (user)
DROP TRIGGER IF EXISTS adjust_user_rating_after_insert_rate;
DELIMITER $$
CREATE TRIGGER adjust_user_rating_after_insert_rate BEFORE UPDATE ON user FOR EACH ROW
BEGIN
	IF (total_rating < NEW.total_rating) THEN
		UPDATE user SET NEW.rating_count = rating_count + 1 WHERE username = NEW.username;
	ELSEIF (total_rating > NEW.total_rating) THEN
		UPDATE user SET NEW.rating_count = rating_count - 1 WHERE username = NEW.username;
    END IF;
    UPDATE user SET NEW.average_rating = total_rating / rating_count;
END$$
DELIMITER ;

-- Trigger: change rating_count by 1 and recalculate average rating when total rating changes (item)
DROP TRIGGER IF EXISTS adjust_item_rating_after_update_rate;
DELIMITER $$
CREATE TRIGGER adjust_item_rating_after_update_rate BEFORE UPDATE ON item FOR EACH ROW
BEGIN
	IF (total_rating < NEW.total_rating) THEN
		UPDATE item SET NEW.rating_count = rating_count + 1 WHERE id = NEW.id;
	ELSEIF (total_rating > NEW.total_rating) THEN
		UPDATE item SET NEW.rating_count = rating_count - 1 WHERE id = NEW.id;
    END IF;
    UPDATE item SET NEW.average_rating = total_rating / rating_count;
END$$
DELIMITER ;
*/