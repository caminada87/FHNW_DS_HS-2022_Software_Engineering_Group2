import json


def test_prediction(app, client, auth):
    """Tests if the Predictor works."""
    auth.login()

    response = client.put(
        '/HousePricePrediction?longitude=8.247756856706363&latitude='
        '47.44192855&postal_code=5244&city=Birrhard&bulding_category='
        'Einfamilienhaus&build_year=1990&living_area=187&num_rooms='
        '6.5&user_id=1'
    )

    response_dict: dict = json.loads(response.data.decode("utf-8"))
    print(response_dict)
    response_expected: dict = {"predicted_price": 1050000}

    assert response_dict == response_expected
