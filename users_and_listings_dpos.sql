USE community_rentals;

-- Database programming objects for users and listings


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



-- signup
-- trigger (before insert on user table): create address in address table if doesn't exist
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



-- retrieve user info
-- get all attributes of user
DROP PROCEDURE IF EXISTS get_user_info;
DELIMITER $$
CREATE PROCEDURE get_user_info( IN username_p VARCHAR(64) )
	BEGIN
		SELECT * FROM user
            WHERE user.username = username_p;
    END $$
DELIMITER ;



-- update user info
-- trigger (before update on user): create new address in address table 
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

-- update name
DROP PROCEDURE IF EXISTS update_user_name;
DELIMITER $$
CREATE PROCEDURE update_user_name( IN username_p VARCHAR(64), 
	IN first_name_p VARCHAR(50), IN last_name_p VARCHAR(50) )
	BEGIN
		UPDATE user SET
			first_name = first_name_p, last_name = last_name_p
            WHERE username = username_p;
    END $$
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

-- update user type
DROP PROCEDURE IF EXISTS update_user_type;
DELIMITER $$
CREATE PROCEDURE update_user_type( IN username_p VARCHAR(64), 
	IN is_seller_p BOOL )
    BEGIN
		UPDATE user SET 
			is_seller = is_seller_p
            WHERE username = username_p;
    END $$
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



-- add payment info
-- trigger (before insert on payment_info): insert new payment type into payment_type if doesn't exist
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



-- add payment preference
-- trigger (before insert on payment_preference): insert new payment type into payment_type if doesn't exist
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
DELETE FROM payment_type WHERE type = "mastercard";

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




-- retrieve listings
-- get all listings for user