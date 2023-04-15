USE community_rentals;


-- Database programming objects for community rental project

-- *******************************************************************************************
-- Triggers:

-- Before insert on user table: create address in address table if doesn't exist
DROP TRIGGER IF EXISTS address_before_insert_user;
DELIMITER $$
CREATE TRIGGER address_before_insert_user
	-- update address table before new tuple added to user table
	BEFORE INSERT ON user
    FOR EACH ROW
    BEGIN
		-- add address to address table if not yet exists
        IF NOT EXISTS (SELECT * FROM address WHERE number = NEW.street_number
			AND street = NEW.street_name AND city = NEW.city 
            AND state = NEW.state AND zipcode = NEW.zipcode) THEN
            
			INSERT INTO address VALUES
				(NEW.street_number, NEW.street_name, NEW.city, 
                NEW.state, NEW.zipcode);
		END IF;
    
    END $$
DELIMITER ;


-- Before update on user: create new address in address table 
-- create new address, not updating in case multiple people live at same address
DROP TRIGGER IF EXISTS address_before_update_user;
DELIMITER $$
CREATE TRIGGER address_before_update_user
	-- update address table before user address is updated
	BEFORE UPDATE ON user
    FOR EACH ROW
    BEGIN
		-- add address to address table if not yet exists
        IF NOT EXISTS (SELECT * FROM address WHERE number = NEW.street_number
			AND street = NEW.street_name AND city = NEW.city 
            AND state = NEW.state AND zipcode = NEW.zipcode) THEN
            
			INSERT INTO address VALUES
				(NEW.street_number, NEW.street_name, NEW.city, 
                NEW.state, NEW.zipcode);
		END IF;
    
    END $$
DELIMITER ;


-- Before insert on payment_info: insert new payment type into payment_type if doesn't exist
DROP TRIGGER IF EXISTS payment_type_before_insert_payment_info;
DELIMITER $$
CREATE TRIGGER payment_type_before_insert_payment_info
	-- update payment_type table before insert to payment_info
	BEFORE INSERT ON payment_info
    FOR EACH ROW
    BEGIN
		-- add payment type to payment_type table if not yet exists
        IF NOT EXISTS (SELECT * FROM payment_type WHERE type = NEW.type) 
			THEN
            INSERT INTO payment_type VALUES
				(NEW.type);
		END IF;
    
    END $$
DELIMITER ;


-- Before insert on payment_preference: insert new payment type into payment_type if doesn't exist
DROP TRIGGER IF EXISTS payment_type_before_insert_payment_preference;
DELIMITER $$
CREATE TRIGGER payment_type_before_insert_payment_preference
	-- update payment_type table before insert to payment_preference
	BEFORE INSERT ON payment_preference
    FOR EACH ROW
    BEGIN
		-- add payment type to payment_type table if not yet exists
        IF NOT EXISTS (SELECT * FROM payment_type WHERE type = NEW.type) 
			THEN
            INSERT INTO payment_type VALUES
				(NEW.type);
		END IF;
    END $$
DELIMITER ;


-- Before insert into item: add to item_category if doesn't exist
DROP TRIGGER IF EXISTS item_category_before_item;
DELIMITER $$
CREATE TRIGGER item_category_before_item
	-- update item_category table before insert to item
	BEFORE INSERT ON item
    FOR EACH ROW
    BEGIN
		-- add new category if not yet exists
        IF NOT EXISTS (SELECT * FROM item_category WHERE category = NEW.category) 
			THEN
            INSERT INTO item_category VALUES
				(NEW.category);
		END IF;
    END $$
DELIMITER ;




-- *******************************************************************************************
-- Basic SELECT Procedures:

-- login
-- check user table for matching username and password
DROP PROCEDURE IF EXISTS login;
DELIMITER $$
CREATE PROCEDURE login( IN username_p VARCHAR(64), IN password_p VARCHAR(128) )
	BEGIN
		
        SELECT * FROM user
			WHERE username = username_p
            AND password = password_p;
    
    END $$
DELIMITER ;


-- Search for user by username/firstname/lastname
DROP PROCEDURE IF EXISTS search_user;
DELIMITER $$
CREATE PROCEDURE search_user(name_p VARCHAR(64))
BEGIN
	SELECT * FROM user HAVING username = name_p OR first_name = name_p OR last_name = name_p;
END$$
DELIMITER ;
call search_user('amazon');

-- retrieve user info
-- get all attributes of user based on username
DROP PROCEDURE IF EXISTS get_user_info;
DELIMITER $$
CREATE PROCEDURE get_user_info( IN username_p VARCHAR(64) )
	BEGIN
		SELECT * FROM user
            WHERE user.username = username_p;
    END $$
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


-- Search for all addresses
DROP PROCEDURE IF EXISTS all_addresses;
DELIMITER $$
CREATE PROCEDURE all_addresses()
BEGIN
	SELECT * FROM address;
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


-- get user's payment info
DROP PROCEDURE IF EXISTS get_user_payment_info;
DELIMITER $$
CREATE PROCEDURE get_user_payment_info( IN username_p VARCHAR(64) )
	BEGIN
		SELECT cc_number, expiration_date, type FROM user_payment
			JOIN payment_info 
            ON user_payment.payment_info = payment_info.cc_number
			WHERE user = username_p;
    END $$
DELIMITER ;


-- get user's payment preferences
DROP PROCEDURE IF EXISTS get_user_payment_preference;
DELIMITER $$
CREATE PROCEDURE get_user_payment_preference( IN username_p VARCHAR(64) )
	BEGIN
		SELECT * FROM payment_preference
			WHERE seller = username_p;
    END $$
DELIMITER ;


-- Search for all items
DROP PROCEDURE IF EXISTS all_items;
DELIMITER $$
CREATE PROCEDURE all_items()
BEGIN
	SELECT * FROM item;
END$$
DELIMITER ;


-- Search for all item categories
DROP PROCEDURE IF EXISTS all_categories;
DELIMITER $$
CREATE PROCEDURE all_categories()
BEGIN
	SELECT * FROM item_category;
END$$
DELIMITER ;


-- Search for all items in a category
DROP PROCEDURE IF EXISTS search_items_by_category;
DELIMITER $$
CREATE PROCEDURE search_items_by_category(category_p VARCHAR(50))
BEGIN
	SELECT * FROM item WHERE category = category_p;
END$$
DELIMITER ;

-- Search for all items owned by seller
DROP PROCEDURE IF EXISTS search_items_by_seller;
DELIMITER $$
CREATE PROCEDURE search_items_by_seller(seller_p VARCHAR(64))
BEGIN
	SELECT * FROM item WHERE owner = seller_p;
END$$
DELIMITER ;

-- Search for specific item by ID
DROP PROCEDURE IF EXISTS search_item_by_id;
DELIMITER $$
CREATE PROCEDURE search_item_by_id(id_p INT)
BEGIN
	SELECT * FROM item WHERE id = id_p;
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


-- retrieve listings
-- get all listings for user
DROP PROCEDURE IF EXISTS get_user_listings;
DELIMITER $$
CREATE PROCEDURE get_user_listings( IN username_p VARCHAR(64) )
	BEGIN
		SELECT item, owner, description, price, quantity, average_rating, 
			rating_count, total_rating, category FROM listing
			JOIN item ON listing.item = item.id
            WHERE owner = username_p;
    END $$
DELIMITER ;


-- Search for all rentals
DROP PROCEDURE IF EXISTS all_rentals;
DELIMITER $$
CREATE PROCEDURE all_rentals()
BEGIN
	SELECT * FROM item JOIN rental ON item.id = rental.item;
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



-- *******************************************************************************************
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
    SELECT COUNT(*) INTO listing_count 
		FROM listing 
        JOIN item ON listing.item = item.id
        WHERE owner = seller_p;
	RETURN (listing_count);
END$$
DELIMITER ;


-- Returns the owner of the specified item
DROP FUNCTION IF EXISTS get_item_owner;
DELIMITER $$
CREATE FUNCTION get_item_owner(item_p INT)
RETURNS VARCHAR(64) DETERMINISTIC READS SQL DATA
BEGIN
	DECLARE item_owner VARCHAR(64) DEFAULT NULL;
    SELECT owner INTO item_owner FROM item WHERE id = item_p;
    RETURN (item_owner);
END$$
DELIMITER ;


-- Returns matching username's password
DROP FUNCTION IF EXISTS get_user_password;
DELIMITER $$
CREATE FUNCTION get_user_password( username_p VARCHAR(64) )
	RETURNS VARCHAR(128)
    DETERMINISTIC
    READS SQL DATA
    BEGIN
		DECLARE user_password VARCHAR(128) DEFAULT NULL;
        SELECT password INTO user_password
			FROM user
            WHERE username = username_p;
		RETURN (user_password);
	END $$
DELIMITER ;



-- *******************************************************************************************
-- INSERTs/DELETEs:

-- signup
-- insert new user to user table
DROP PROCEDURE IF EXISTS signup;
DELIMITER $$
CREATE PROCEDURE signup( IN username_p VARCHAR(64), IN password_p VARCHAR(128),
	IN first_name_p VARCHAR(50), IN last_name_p VARCHAR(50), 
    IN phone_p VARCHAR(11), IN is_customer_p BOOL, IN is_seller_p BOOL, 
    IN street_num_p INT, IN street_name_p VARCHAR(50), IN city_p VARCHAR(50), 
    IN state_p CHAR(2), IN zipcode_p CHAR(5) )
    BEGIN
		-- local variable w/ default value for checking duplicate entry
        DECLARE duplicate_username TINYINT DEFAULT FALSE;
        
        BEGIN 
			-- exit handler to check for duplicate username
			DECLARE EXIT HANDLER FOR 1062
				-- username already exists
				SET duplicate_username = TRUE;
		END;
        
		-- try inserting new user to user table
		INSERT INTO user (username, password, first_name, last_name, phone, 
			average_rating, is_customer, is_seller, street_number, 
			street_name, city, state, zipcode) VALUES
			(username_p, password_p, first_name_p, last_name_p, phone_p, "5",
			is_customer_p, is_seller_p, street_num_p, street_name_p,
			city_p, state_p, zipcode_p);
		
		-- no duplicates: add new tuple to user table and print statement
		SELECT ("1 ROW INSERTED");

    END $$
DELIMITER ;


-- add payment info
-- insert new payment info to payment_info table and associate
-- user to payment in user_payment table
DROP PROCEDURE IF EXISTS user_adds_payment_info;
DELIMITER $$
CREATE PROCEDURE user_adds_payment_info( IN username_p VARCHAR(64),
	IN cc_number_p VARCHAR(16), IN expiration_date_p DATE,
    IN type_p ENUM('VISA','AMERICAN EXPRESS','MASTERCARD') )
    BEGIN    
		-- insert new cc info to payment_info table if doesn't exist
        IF NOT EXISTS (SELECT * FROM payment_info WHERE 
			cc_number = cc_number_p) THEN
            INSERT INTO payment_info VALUES
			(cc_number_p, expiration_date_p, type_p);
		
        -- update payment info if cc number already exists
        ELSE UPDATE payment_info SET expiration_date = expiration_date_p,
			type = type_p WHERE cc_number = cc_number_p;
        END IF;
        
        -- associate user to payment info in user_payment table if
        -- not duplicate
        IF NOT EXISTS (SELECT * FROM user_payment WHERE
			user = username_p AND payment_info = cc_number_p)
            THEN 
				INSERT INTO user_payment VALUES
				(username_p, cc_number_p);
		END IF;
	END $$
DELIMITER ;


-- add payment preference
-- insert new payment preference for seller
DROP PROCEDURE IF EXISTS user_adds_payment_preference;
DELIMITER $$
CREATE PROCEDURE user_adds_payment_preference( IN username_p VARCHAR(64),
	IN type_p ENUM('VISA','AMERICAN EXPRESS','MASTERCARD') )
	BEGIN
		-- ensure user is seller
        IF EXISTS (SELECT * FROM user WHERE username = username_p 
			AND is_seller = TRUE) THEN
            
			-- associate user to payment preference if not already associated
            IF NOT EXISTS (SELECT * FROM payment_preference WHERE seller = username_p
				AND type = type_p) THEN
                
                INSERT INTO payment_preference VALUES
				(username_p, type_p);
                
                SELECT("Payment preference added for user");
			END IF;
		ELSE
			SELECT("User is not a seller");
		END IF;
    END $$
DELIMITER ;


-- user deletes payment info
-- delete user's association to payment info
DROP PROCEDURE IF EXISTS user_deletes_payment_info;
DELIMITER $$
CREATE PROCEDURE user_deletes_payment_info( IN username_p VARCHAR(64),
	IN cc_number_p VARCHAR(16) )
    BEGIN
        -- delete user and payment info association from user_payment table
        IF EXISTS (SELECT * FROM user_payment WHERE
			user = username_p AND payment_info = cc_number_p)
            THEN 
				DELETE FROM user_payment WHERE
				user = username_p AND payment_info = cc_number_p;
		END IF;
	END $$
DELIMITER ;


-- user deletes payment preference
-- delete user's association to payment type preference
DROP PROCEDURE IF EXISTS user_deletes_payment_preference;
DELIMITER $$
CREATE PROCEDURE user_deletes_payment_preference( IN username_p VARCHAR(64),
	IN type_p ENUM('VISA','AMERICAN EXPRESS','MASTERCARD') )
    BEGIN
		-- delete user and payment type association from payment_preference table
        IF EXISTS (SELECT * FROM payment_preference WHERE
			seller = username_p AND type = type_p)
            THEN
				DELETE FROM payment_preference WHERE
                seller = username_p AND type = type_p;
		END IF;
    END $$
DELIMITER ;


-- create new listing
-- use item that already exists in item table
DROP PROCEDURE IF EXISTS create_listing;
DELIMITER $$
CREATE PROCEDURE create_listing(username_p VARCHAR(64), item_p INT, price_p DECIMAL(13,2), quantity_p INT)
BEGIN
	-- ensure user creating the item actually owns the item
	IF EXISTS (SELECT(get_item_owner(item_p))) THEN
		IF NOT (username_p = get_item_owner(item_p)) THEN
			SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = "User does not own this item";
		END IF;
	ELSE
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = "Item does not exist";
	END IF;
    
	-- set user to seller before creating new listing
	IF EXISTS (SELECT * FROM user WHERE username = username_p AND is_seller = FALSE) THEN
		UPDATE user SET is_seller = TRUE WHERE username = username_p;
	END IF;
    
    INSERT INTO listing VALUES (item_p, price_p, quantity_p);
        
	SELECT("Listing created");
END$$
DELIMITER ;


-- create new listing
-- insert new item to item table and create new listing in listing table
DROP PROCEDURE IF EXISTS create_new_item_listing;
DELIMITER $$
CREATE PROCEDURE create_new_item_listing( IN username_p VARCHAR(64),
	IN item_description_p TEXT(1000), IN category_p VARCHAR(50),  
    IN price_p DECIMAL(13,2), IN quantity_p INT )
    BEGIN
		-- local variable to hold PK of new item
        DECLARE new_item INT;
        
		-- set user to seller before creating new listing
        IF EXISTS (SELECT * FROM user WHERE username = username_p AND is_seller = FALSE) THEN
			UPDATE user SET is_seller = TRUE WHERE username = username_p;
		END IF;
            
		-- create new item
		INSERT INTO item (owner, description, average_rating, category)
			VALUES (username_p, item_description_p, "0", category_p);
			
		-- store new item's PK into new_item variable
		SELECT LAST_INSERT_ID() INTO new_item;
		
		-- create new listing with new item
		INSERT INTO listing VALUES
			(new_item, price_p, quantity_p);
		
		SELECT("Listing created");
    END $$
DELIMITER ;


-- delete listing
-- delete listing from listing table
DROP PROCEDURE IF EXISTS delete_listing;
DELIMITER $$
CREATE PROCEDURE delete_listing( IN item_p INT, IN username_p VARCHAR(64) )
	BEGIN
		-- ensure user deleting the listing actually owns the item
		IF EXISTS (SELECT(get_item_owner(item_p))) THEN
			IF NOT (username_p = get_item_owner(item_p)) THEN
				SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = "User does not own this item";
			END IF;
		ELSE
			SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = "Item does not exist";
		END IF;
        
		-- delete listing
		DELETE FROM listing WHERE item = item_p;
    END $$
DELIMITER ;


-- create item
DROP PROCEDURE IF EXISTS create_item;
DELIMITER $$
CREATE PROCEDURE create_item( IN username_p VARCHAR(64), IN description_p TEXT(1000),
	IN category_p VARCHAR(50) )
    BEGIN
		-- set user to seller before creating new item
        IF EXISTS (SELECT * FROM user WHERE username = username_p AND is_seller = FALSE) THEN
			UPDATE user SET is_seller = TRUE WHERE username = username_p;
		END IF;
            
		-- create new item
		INSERT INTO item (owner, description, average_rating, category)
			VALUES (username_p, description_p, "0", category_p);
    END $$
DELIMITER ;


-- delete item from item table
DROP PROCEDURE IF EXISTS delete_item;
DELIMITER $$
CREATE PROCEDURE delete_item( IN item_p INT, IN username_p VARCHAR(64) )
	BEGIN
		-- ensure user deleting the item actually owns the item
		IF EXISTS (SELECT(get_item_owner(item_p))) THEN
			IF NOT (username_p = get_item_owner(item_p)) THEN
				SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = "User does not own this item";
			END IF;
		ELSE
			SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = "Item does not exist";
		END IF;
        
		-- delete item
		DELETE FROM item WHERE id = item_p;
    END $$
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
	ELSEIF (renter_p = get_item_owner(item_p)) THEN
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = 'User cannot rent their own item';
	ELSE
		INSERT INTO rental VALUES (item_p, renter_p, payment_p, rent_date, return_date);
        UPDATE listing SET quantity = quantity - 1 WHERE item = item_p;
        IF (num_item_listed(item_p) <= 0) THEN
			DELETE FROM listing WHERE item = item_p;
        END IF;
    END IF;
END$$
DELIMITER ;



-- *******************************************************************************************
-- UPDATEs:

-- update user info
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


-- update phone 
DROP PROCEDURE IF EXISTS update_user_phone;
DELIMITER $$
CREATE PROCEDURE update_user_phone( IN username_p VARCHAR(64),
	IN phone_p VARCHAR(11) )
    BEGIN
		UPDATE user SET 
			phone = phone_p
            WHERE username = username_p;
    END $$
DELIMITER ;


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


-- update address
DROP PROCEDURE IF EXISTS update_user_address;
DELIMITER $$
CREATE PROCEDURE update_user_address( IN username_p VARCHAR(64),
	IN street_num_p INT, IN street_name_p VARCHAR(50),
    IN city_p VARCHAR(50), IN state_p VARCHAR(50),
    IN zipcode_p CHAR(5) )
    BEGIN
		UPDATE user SET
			street_number = street_num_p,
            street_name = street_name_p,
            city = city_p, state = state_p,
            zipcode = zipcode_p
            WHERE username = username_p;
    END $$
DELIMITER ;


-- update listing
-- update price from listing table
-- update quantity from listing table
-- update item description for item associated to listing
DROP PROCEDURE IF EXISTS update_listing;
DELIMITER $$
CREATE PROCEDURE update_listing( IN item_p INT, IN username_p VARCHAR(64),
	IN new_price_p DECIMAL(13,2), IN new_quantity_p INT, 
    IN new_item_description_p TEXT(1000) )
	BEGIN
		IF EXISTS (SELECT * FROM listing WHERE item = item_p) THEN
			-- ensure user deleting the item actually owns the item
			IF EXISTS (SELECT(get_item_owner(item_p))) THEN
				IF NOT (username_p = get_item_owner(item_p)) THEN
					SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = "User does not own the listed item";
				END IF;
			ELSE
				SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = "Item does not exist";
			END IF;
            
            -- update price and quantity in listing to new values
            UPDATE listing SET price = new_price_p, 
				quantity = new_quantity_p WHERE
                item = item_p;
            
            -- update item description for item associated to listing
			UPDATE item SET description = new_item_description_p
				WHERE id = item_p;
				
		END IF;
    END $$
DELIMITER ;



-- Rate item
DROP PROCEDURE IF EXISTS rate_item;
DELIMITER $$
CREATE PROCEDURE rate_item(rater_p VARCHAR(64), item_p INT, rating_p INT)
BEGIN
	IF (rater_p = get_item_owner(item_p)) THEN
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = 'User cannot rate their own item';
	ELSEIF (rating_p > 5 OR rating_p < 1) THEN
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
CREATE PROCEDURE rate_user(rater_p VARCHAR(64), user_p VARCHAR(64), rating_p INT)
BEGIN
	IF (user_p = rater_p) THEN
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = 'User cannot rate themself';
	ELSEIF (rating_p > 5 OR rating_p < 1) THEN
		SIGNAL SQLSTATE '42000' SET MESSAGE_TEXT = 'Ratings must be between 1 and 5';
	ELSE
		UPDATE user SET total_rating = total_rating + rating_p WHERE username = user_p;
        UPDATE user SET rating_count = rating_count + 1 WHERE username = user_p;
        UPDATE user SET average_rating = total_rating / rating_count WHERE username = user_p;
    END IF;
END$$
DELIMITER ;
