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


-- retrieve listings
-- get all listings for user