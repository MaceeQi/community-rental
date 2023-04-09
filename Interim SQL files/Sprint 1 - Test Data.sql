USE community_rentals;

INSERT INTO address VALUES
	(38, 'Westland Ave.', 'Boston', 'MA', 02115),
    (1, 'North College St.', 'Northfield', 'MN', 55057)
;

INSERT INTO payment_type VALUES
	('VISA'),
    ('MASTERCARD'),
    ('AMERICAN EXPRESS')
;

INSERT INTO payment_info VALUES
	(1111222233334444, '2026-01-01', 'VISA'),
    (9999888877776666, '2025-12-12', 'MASTERCARD')
;

INSERT INTO user (username, password, first_name, last_name, phone, average_rating, is_customer, is_seller,
				street_number, street_name, city, state, zipcode) VALUES
	('elongated', 'muskrat', 'Elon', 'Musk', 123456789, 0, FALSE, TRUE, 38, 'Westland Ave.', 'Boston', 'MA', 02115),
    ('amazon', 'webservices', 'Jose', 'Annunziato', 0000000, 0, TRUE, FALSE, 1, 'North College St.', 'Northfield', 'MN', 55057)
;

INSERT INTO user_payment VALUES
	('elongated', 1111222233334444),
    ('amazon', 9999888877776666)
;

INSERT INTO payment_preference VALUES
	('elongated', 'MASTERCARD')
;

INSERT INTO item_category VALUES
	('technology'),
    ('furniture'),
    ('cooking')
;

INSERT INTO item (description, average_rating, category) VALUES
	('2017 macbook pro, lightly used', 0, 'technology'),
    ('brand new IKEA desk chair', 0, 'furniture'),
    ('wok', 0, 'cooking'),
    ('butter knife', 0, 'cooking'),
    ('computer desk', 0, 'furniture')
;

INSERT INTO wishlist VALUES
    (2, 'amazon'),
    (4, 'amazon')
;

INSERT INTO listing VALUES
	(1, 'elongated', 9999, 1),
    (3, 'elongated', 35.99, 2)
;

INSERT INTO rental VALUES
	(1, 'amazon', 1111222233334444, '2023-04-04', '2023-04-21')
;