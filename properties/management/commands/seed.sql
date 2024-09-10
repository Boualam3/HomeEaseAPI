
INSERT INTO core_user (id, username, password, email, is_staff, is_superuser, is_active, date_joined, first_name, last_name)
VALUES (1, 'host_user', 'pbkdf2_sha256$870000$PdoKpYaaWKmxjTsZwzyp0G$W2QWgP9WTier4mDlzfgpmcVId6hJ3q+hvzc9zG3QE3s=', 'host@example.com', 0, 0, 1, '2023-01-01', 'Host', 'User'),
       (2, 'guest_user', 'pbkdf2_sha256$870000$amectQviRiuUWx0GecVXxN$UYKOZPPfiEnsH3eXTLyEtqH6Bg5WXzH7wbM2c4j+d2c=', 'guest@example.com', 0, 0, 1, '2023-01-01', 'Guest', 'User');

INSERT INTO core_profile (id, user_id, role, phone_number, street, city, zip)
VALUES (1, 1, 'HOST', '1234567890', '123 Host St', 'Hostville', '12345'),
       (2, 2, 'GUEST', '0987654321', '456 Guest St', 'Guestville', '54321');

INSERT INTO properties_category (id, title)
VALUES (1, 'Luxury'), (2, 'Budget'), (3, 'Eco-friendly');

INSERT INTO properties_property (id, title, slug, description, property_type, host_id, category_id, location, price, number_of_bedrooms, number_of_bathrooms, property_size, amenities, availability, from_date, to_date, number_of_guests, last_update)
VALUES 
(1, 'Luxury Beach House', 'luxury-beach-house', 'A luxurious house on the beach.', 'HOME',  1, 1, 'Miami, FL', 450.00, 4, 3, 2000, 'Pool, Wifi, Ocean View', true, '2023-01-01', '2023-12-31', 8, '2023-01-01'),
(2, 'Cozy Mountain Cabin', 'cozy-mountain-cabin', 'A cozy cabin in the mountains.', 'CABIN', 1, 3, 'Aspen, CO', 300.00, 3, 2, 1500, 'Fireplace, Hot Tub, Mountain View', true, '2023-01-01', '2023-12-31', 6, '2023-01-01'),
(3, 'Urban Apartment', 'urban-apartment', 'A stylish apartment in the city center.', 'APARTMENT', 1, 2, 'New York, NY', 350.00, 2, 2, 1200, 'Wifi, Central Heating', true, '2023-01-01', '2023-12-31', 4, '2023-01-01');

INSERT INTO properties_review (id, property_id, profile_id, reviewer_name, rating, description, date)
VALUES 
(1, 1, 2, 'guest_user', 5, 'Amazing stay at the beach house! Highly recommend.', '2023-05-01'),
(2, 3, 2, 'guest_user', 4, 'Great location in the city, but the price was a bit high.', '2023-05-10'),
(3, 2, 2, 'guest_user', 5, 'The mountain cabin was perfect for a weekend retreat.', '2023-06-01');
