USE community_rentals;

-- Test basic procedures
-- all_addresses()
CALL all_addresses();

-- all_items()
CALL all_items();

-- search_items(category)
CALL search_items('technology');
CALL search_items('cooking');
CALL search_items('furniture');

-- all_listings()
CALL all_listings();

-- seller_listings(seller)
CALL seller_listings('elongated');

-- all_rentals()
CALL all_rentals();

-- all_users()
CALL all_users();

-- all_customers()
CALL all_customers();

-- all_sellers()
CALL all_sellers();

-- all_payment_info()
CALL all_payment_info();

-- all_user_payment()
CALL all_user_payment();

-- search_user_username(username)
CALL search_user('elongated');
CALL search_user('Elon');
CALL search_user('Musk');
CALL search_user('amazon');
CALL search_user('Jose');
CALL search_user('Annunziato');

-- list_wishlist(username)
CALL list_wishlist('amazon');



-- Test helper functions
-- user_is_customer(username)
SELECT(user_is_customer('elongated'));	-- 0 = FALSE
SELECT(user_is_customer('amazon'));		-- 1 = TRUE

-- user_is_seller(username)
SELECT(user_is_seller('elongated'));	
SELECT(user_is_seller('amazon'));	

-- item_in_listing(item_id)
SELECT(item_in_listing(1));
SELECT(item_in_listing(2));
SELECT(item_in_listing(3));
SELECT(item_in_listing(4));
SELECT(item_in_listing(5));

-- user_payment_exists(username, payment_number)
SELECT(user_payment_exists('elongated', 1111222233334444));
SELECT(user_payment_exists('elongated', 9999888877776666));
SELECT(user_payment_exists('amazon', 1111222233334444));
SELECT(user_payment_exists('amazon', 9999888877776666));

-- num_item_listed(item_id)
SELECT(num_item_listed(1));
SELECT(num_item_listed(2));
SELECT(num_item_listed(3));

-- seller_listing_count(seller_p)
SELECT(seller_listing_count('elongated'));


-- Test insert/delete procedures
-- rent_item(item, username, payment, rent_date, return_date)
CALL all_rentals();		-- should just be item #1
CALL all_listings();	-- should be items #1 and #3 with quantities 1 and 2, respectively
CALL rent_item(3, 'amazon', 9999888877776666, '2023-04-07', '2024-01-01');
CALL all_rentals();		-- should now be items #1 and #3
CALL all_listings();	-- item #3 should have quantity - 1
CALL rent_item(1, 'amazon', 9999888877776666, '2023-04-07', '2024-01-01');
CALL all_rentals();		-- should now be items #1 (twice) and #3
CALL all_listings();	-- item #1 should now be gone

CALL rent_item(3, 'elongated', 9999888877776666, '2023-04-07', '2024-01-01'); 	-- should be a non-customer error
CALL rent_item(2, 'amazon', 9999888877776666, '2023-04-07', '2024-01-01');		-- should be an item-not-found error
CALL rent_item(3, 'amazon', 1111222233334444, '2023-04-07', '2024-01-01');		-- should be an invalid-payment error
CALL rent_item(3, 'amazon', 9999888877776666, '2024-01-01', '2023-04-07');		-- should be an invalid date error

-- rate_item(item_id, rating)
CALL all_items();		-- all items have average_rating = rating_count = total_rating = 0.0
CALL rate_item(5, 5);
CALL all_items();		-- item #5 should now have average rating = 5.0, with 1 rating and total_rating = 5
CALL rate_item(5, 3);
CALL rate_item(5, 2);
CALL all_items();		-- item #5 should now have average rating = 3.3, with 3 ratings and total_rating = 10
CALL rate_item(5, 0);	-- should be an invalid-rating error
CALL rate_item(5, 6);	-- should be an invalid-rating error

-- rate_user(username, rating)
CALL all_users();		-- all users have average_rating = rating_count = total_rating = 0.0
CALL rate_user('elongated', 5);
CALL all_users();		-- elon musk should now have average rating = 5.0, with 1 rating and total_rating = 5
CALL rate_user('elongated', 3);
CALL rate_user('elongated', 2);
CALL all_users();		-- elon musk should now have average rating = 3.3, with 3 ratings and total_rating = 10
CALL rate_user('elongated', 0);	-- should be an invalid-rating error
CALL rate_user('elongated', 6);	-- should be an invalid-rating error

-- wish_for_item(username, item)
CALL list_wishlist('amazon');			-- should have 2 items (items #2 and #4)
CALL wish_for_item('amazon', 3);
CALL list_wishlist('amazon');			-- should have 3 items (items #2, #3, and #4)
CALL wish_for_item('amazon', 3);		-- should be a duplicate-wish error
CALL wish_for_item('amazooooon', 3);	-- should be a nonexistent-user error
CALL wish_for_item('elongated', 3);		-- should be a non-customer error
CALL wish_for_item('amazon', 6);		-- should be a nonexistent-item error

-- delete_wishlist_item(username, item)
CALL list_wishlist('amazon');			-- should have 3 items (items #2, #3, and #4)
CALL delete_wishlist_item('amazon', 2);
CALL list_wishlist('amazon');			-- should have 2 items (items #3 and #4)
CALL delete_wishlist_item('amazon', 2);	-- should be an nonexistent-entry error

-- add_payment_info(ccnumber, exp_date, card_type)
CALL all_payment_info();		-- should just be 1 VISA and 1 MASTERCARD
CALL add_payment_info(2222444466668888, '2027-08-08', 'AMERICAN EXPRESS');
CALL all_payment_info();		-- new card should be in there

-- del_payment_info(ccnumber)
CALL all_payment_info();		-- should just be 1 of each card type
CALL del_payment_info(2222444466668888);
CALL all_payment_info();		-- back to the OG 2

-- add_user_payment(username, ccnumber)
CALL all_payment_info();		-- should just be 1 VISA and 1 MASTERCARD
CALL add_payment_info(2222444466668888, '2027-08-08', 'AMERICAN EXPRESS');
CALL all_payment_info();		-- new card should be in there
CALL all_user_payment();		-- 2 users with 1 payment_info each
CALL add_user_payment('amazon', 2222444466668888);
CALL all_user_payment();		-- 'amazon' now has a second payment_info

-- del_user_payment(username, ccnumber)
CALL all_user_payment();		-- 'elongated' has 1 payment_info, 'amazon' has 2
CALL del_user_payment('amazon', 2222444466668888);
CALL all_user_payment();		-- 'amazon' should be back to 1 payment_info


-- Test update procedures
-- update_user_seller(username_p)
CALL all_sellers();
CALL all_customers();		-- 1 seller and 1 customer
CALL update_user_seller('amazon', TRUE);
CALL all_sellers();			-- 'amazon' is now also a seller
CALL all_customers();		-- and is still a customer
CALL update_user_seller('elongated', FALSE);	-- should get an error
CALL update_user_seller('amazon', FALSE);

-- update_user_customer(username_p)
CALL all_sellers();
CALL all_customers();		-- 1 seller and 1 customer
CALL update_user_customer('elongated', TRUE);
CALL all_customers();			-- 'elongated' is now also a customer
CALL all_sellers();		-- and is still a seller
CALL update_user_customer('elongated', FALSE);

-- update_user_first_name(username, first_name_p)
CALL all_users();		-- 'Jose Annunziato' and 'Elon Musk'
CALL update_user_first_name('elongated', 'Yena');
CALL update_user_first_name('amazon', 'Yutong');
CALL all_users();		-- 'Yutong Annunziato' and 'Yena Musk'

-- update_user_last_name(username, last_name_p)
CALL all_users();		-- 'Yutong Annunziato' and 'Yena Musk'
CALL update_user_last_name('elongated', 'Shin');
CALL update_user_last_name('amazon', 'He');
CALL all_users();		-- 'Yutong He' and 'Yena Shin'
CALL update_user_first_name('elongated', 'Elon');
CALL update_user_last_name('elongated', 'Musk');
CALL update_user_first_name('amazon', 'Jose');
CALL update_user_last_name('amazon', 'Annunziato');


-- update_user_address(number, street, city, state, zipcode)
/* not currently working
CALL all_users();
CALL all_addresses();
DELETE FROM address WHERE number = 101;
CALL update_user_address('elongated', 101, 'Massachusetts Ave.', 'Boston', 'MA', 02110);
*/