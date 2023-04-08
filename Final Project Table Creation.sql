DROP DATABASE IF EXISTS community_rentals;
CREATE DATABASE community_rentals;

USE community_rentals;


CREATE TABLE address (
	number			INT				NOT NULL,
    street			VARCHAR(50)		NOT NULL,
	city			VARCHAR(50)		NOT NULL,
    state			CHAR(2)			NOT NULL,
    zipcode			CHAR(5)			NOT NULL,
    CONSTRAINT address_pk 
		PRIMARY KEY (number, street, city, state, zipcode)
);

CREATE TABLE payment_type (
	type		ENUM('VISA', 'AMERICAN EXPRESS', 'MASTERCARD')	PRIMARY KEY
);


CREATE TABLE payment_info (
	cc_number		VARCHAR(16)		PRIMARY KEY,
    expiration_date DATE			NOT NULL,
    type			ENUM('VISA', 'AMERICAN EXPRESS', 'MASTERCARD')	NOT NULL,
    CONSTRAINT type_fk
		FOREIGN KEY (type)
        REFERENCES payment_type (type)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);


CREATE TABLE user (
	username			VARCHAR(64)		PRIMARY KEY UNIQUE,
    password			VARCHAR(128)	NOT NULL,
	first_name			VARCHAR(50)		NOT NULL,
	last_name			VARCHAR(50)		NOT NULL,
	phone				VARCHAR(11)		NOT NULL,
    average_rating		DECIMAL(2, 1)	NOT NULL,
    rating_count		INT				NOT NULL DEFAULT 0,
    total_rating		INT				NOT NULL DEFAULT 0,
	is_customer			BOOL			DEFAULT TRUE,
    is_seller			BOOL			DEFAULT FALSE,	
	street_number		INT				NOT NULL,
	street_name			VARCHAR(50)		NOT NULL,
	city				VARCHAR(50)		NOT NULL,
	state				CHAR(2)			NOT NULL,
	zipcode				CHAR(5)			NOT NULL,    
    CONSTRAINT address_fk
		FOREIGN KEY (street_number, street_name, city, state, zipcode)
        REFERENCES address (number, street, city, state, zipcode)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE user_payment (
	user			VARCHAR(64)	NOT NULL,
    payment_info	VARCHAR(16)	NOT NULL,
    CONSTRAINT user_payment_fk
		FOREIGN KEY (user)
		REFERENCES user (username)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
    CONSTRAINT info_payment_fk
		FOREIGN KEY (payment_info)
        REFERENCES payment_info (cc_number)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE payment_preference (
	seller		VARCHAR(64)		NOT NULL,
    type		ENUM('VISA', 'AMERICAN EXPRESS', 'MASTERCARD')	NOT NULL,
    CONSTRAINT seller_preference_fk
		FOREIGN KEY (seller)
        REFERENCES user (username)
        ON UPDATE CASCADE
        ON DELETE RESTRICT,
	CONSTRAINT type_preference_fk
		FOREIGN KEY (type)
        REFERENCES payment_type (type)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE item_category (
	category	VARCHAR(50)		PRIMARY KEY
);


CREATE TABLE item (
	id					INT				PRIMARY KEY AUTO_INCREMENT,
    description			TEXT(1000)		NOT NULL,
    average_rating		DECIMAL(2, 1)	NOT NULL,
    rating_count		INT				NOT NULL DEFAULT 0,
    total_rating		INT				NOT NULL DEFAULT 0,
    category			VARCHAR(50)		NOT NULL,
	CONSTRAINT category_fk
		FOREIGN KEY (category)
        REFERENCES item_category (category)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE wishlist (
	item			INT			NOT NULL,
    customer		VARCHAR(64)	NOT NULL,
    CONSTRAINT item_wishlist_fk
		FOREIGN KEY (item)
        REFERENCES item (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
	CONSTRAINT customer_wishlist_fk
		FOREIGN KEY (customer)
        REFERENCES user (username)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);

CREATE TABLE listing (
	item		INT				NOT NULL,
    seller		VARCHAR(64)		NOT NULL,
    price		DECIMAL(13,2)	NOT NULL,
    quantity	INT				NOT NULL,
    CONSTRAINT item_listing_fk
		FOREIGN KEY (item)
        REFERENCES item (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
	CONSTRAINT seller_listing_fk
		FOREIGN KEY (seller)
		REFERENCES user (username)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

CREATE TABLE rental (
	item			INT				NOT NULL,
    customer		VARCHAR(64)		NOT NULL,
    payment			VARCHAR(16)		NOT NULL,
    rental_date		DATE			NOT NULL,
    return_date		DATE			NOT NULL,
    CONSTRAINT item_rental_fk
		FOREIGN KEY (item)
        REFERENCES item (id)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
	CONSTRAINT customer_rental_fk
		FOREIGN KEY (customer)
        REFERENCES user (username)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
	CONSTRAINT payment_rental_fk
		FOREIGN KEY (payment)
        REFERENCES payment_info (cc_number)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);