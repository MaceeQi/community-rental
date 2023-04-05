USE community_rentals;

-- create initial data for database testing

-- address
INSERT INTO address VALUES
	(800, "Boylston St", "Boston", "MA", "02199"),
    (100, "Huntington Ave", "Boston", "MA", "02116");
    
    
-- payment type
INSERT INTO payment_type VALUES
	("Visa"),
    ("Mastercard"),
    ("American Express");
    

-- payment info
INSERT INTO payment_info VALUES
	("123456789112", "2023-05-01", "Visa"),
    ("123456789221", "2023-07-01", "American Express");
    
    
-- user
INSERT INTO user (username, password, first_name, last_name, phone, average_rating,
	is_customer, is_seller, street_number, street_name, city, state, zipcode) 
	VALUES
	("cb123", "c123", "chanon", "bovornvirakit", "987654321", "5", TRUE, TRUE, 
    800, "Boylston St", "Boston", "MA", "02199"),
    ("mq123", "m123", "macee", "qi", "123456789", "5", TRUE, FALSE, 
    100, "Huntington Ave", "Boston", "MA", "02116");
    
    
-- user payment
INSERT INTO user_payment VALUES
	("cb123", "123456789112"),
    ("mq123", "123456789221");
    
    
-- payment preference
INSERT INTO payment_preference VALUES
	("cb123", "visa"),
    ("cb123", "american express");
    
    
-- item category
INSERT INTO item_category VALUES
	("sports equipment"), 
    ("books"),
    ("tools"),
    ("clothing");
    
    
-- item
INSERT INTO item (description, average_rating, category) VALUES
	("mountain bike", "5", "sports equipment"),
    ("algorithms textbook", "5", "books"),
    ("snowboard", "5", "sports equipment"),
    ("database systems textbook by connolly and begg", "5", "books");
    
    
-- wishlist
INSERT INTO wishlist VALUES
	(2, "mq123"),
    (3, "mq123");
    
    
-- listing
INSERT INTO listing VALUES
	(1, "cb123", "50.00", 2),
    (2, "cb123", "75.99", 1),
    (3, "cb123", "99.99", 1),
    (4, "cb123", "28.50", 0);
    
    
-- rental
INSERT INTO rental VALUES
	(4, "mq123", "123456789221", "2023-01-05", "2023-05-01"),
    (3, "mq123", "123456789221", "2022-12-25", "2023-03-08");
    