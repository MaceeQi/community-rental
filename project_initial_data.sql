USE community_rentals;

-- create initial data for database testing

-- address
INSERT INTO address VALUES
	(800, "Boylston St", "Boston", "MA", "02199"),
    (100, "Huntington Ave", "Boston", "MA", "02116"),
    (38, 'Westland Ave.', 'Boston', 'MA', 02115),
    (1, 'North College St.', 'Northfield', 'MN', 55057);
    
    
-- payment type
INSERT INTO payment_type VALUES
	("Visa"),
    ("Mastercard"),
    ("American Express");
    

-- payment info
INSERT INTO payment_info VALUES
	("123456789112", "2023-05-01", "Visa"),
    ("123456789221", "2023-07-01", "American Express"),
    (1111222233334444, '2026-01-01', 'VISA'),
    (9999888877776666, '2025-12-12', 'MASTERCARD');
    
    
-- user
INSERT INTO user (username, password, first_name, last_name, phone, average_rating,
	is_customer, is_seller, street_number, street_name, city, state, zipcode) 
	VALUES
	("cb123", "c123", "chanon", "bovornvirakit", "987654321", "5", TRUE, TRUE, 
    800, "Boylston St", "Boston", "MA", "02199"),
    ("mq123", "m123", "macee", "qi", "123456789", "5", TRUE, FALSE, 
    100, "Huntington Ave", "Boston", "MA", "02116"),
    ('elongated', 'muskrat', 'Elon', 'Musk', 123456789, 0, FALSE, TRUE, 
    38, 'Westland Ave.', 'Boston', 'MA', 02115),
    ('amazon', 'webservices', 'Jose', 'Annunziato', 0000000, 0, TRUE, FALSE, 
    1, 'North College St.', 'Northfield', 'MN', 55057);
    
    
-- user payment
INSERT INTO user_payment VALUES
	("cb123", "123456789112"),
    ("mq123", "123456789221"),
    ('elongated', 1111222233334444),
    ('amazon', 9999888877776666);
    
    
-- payment preference
INSERT INTO payment_preference VALUES
	("cb123", "visa"),
    ("cb123", "american express"),
    ('elongated', 'MASTERCARD');
    
    
-- item category
INSERT INTO item_category VALUES
	("sports equipment"), 
    ("books"),
    ("tools"),
    ("clothing"),
    ('technology'),
    ('furniture'),
    ('cooking');
    
    
-- item
INSERT INTO item (owner, description, average_rating, category) VALUES
	("cb123", "mountain bike", "0", "sports equipment"),
    ("cb123", "algorithms textbook", "0", "books"),
    ("cb123","snowboard", "0", "sports equipment"),
    ("cb123","database systems textbook by connolly and begg", "0", "books"),
    ('2017 macbook pro, lightly used', 'elongated', 0, 'technology'),
    ('brand new IKEA desk chair', 'elongated', 0, 'furniture'),
    ('wok', 'elongated', 0, 'cooking'),
    ('butter knife', 'elongated', 0, 'cooking'),
    ('computer desk', 'elongated', 0, 'furniture');
    
    
-- wishlist
INSERT INTO wishlist VALUES
	(2, "mq123"),
    (3, "mq123"),
    (2, 'amazon'),
    (4, 'amazon');
    
    
-- listing
INSERT INTO listing VALUES
	(1, "50.00", 2),
    (2, "75.99", 1),
    (3, "99.99", 1),
    (4, "28.50", 0),
    (5, 9999, 1),
    (6, 35.99, 2);
    
    
-- rental
INSERT INTO rental VALUES
	(1, 'amazon', 1111222233334444, '2023-04-04', '2023-04-21'),
	(4, "mq123", "123456789221", "2023-01-05", "2023-05-01"),
    (3, "mq123", "123456789221", "2022-12-25", "2023-03-08");
    