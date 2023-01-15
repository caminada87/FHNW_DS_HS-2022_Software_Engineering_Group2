INSERT INTO user (email, permission_id, password)
VALUES ('test@tester.com', 3,
        'pbkdf2:sha256:260000$IioHQNBimvlYay98$d930f1e110f4d5fea3e69ce7251a8c80ea935cbac477d3c23165d51590d9326a');

INSERT INTO predictions (user_id, query_data, predicted_price)
VALUES (1,
        '{"longitude": "8.247756856706363", "latitude": "47.44192855", "postal_code": "5244", "city": "Birrhard", "bulding_category": "Wohnung", "build_year": "1990", "living_area": "187", "num_rooms": "6.5"}',
        '{"predicted_price": 1120000}')