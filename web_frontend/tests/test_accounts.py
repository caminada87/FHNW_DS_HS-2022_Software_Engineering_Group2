import json


def test_accounts_get(client, auth):
    """
    Tests the get method
    """
    auth.login()

    client.post(
        "/auth/register",
        data={
            "email": "b@b.ch",
            "password": "1234",
        },
    )

    response = client.get("/accounts/account?id=11")

    response_dict: dict = json.loads(response.data.decode("utf-8"))
    response_expected: dict = {
        "id": 11,
        "email": "b@b.ch",
        "permission_id": -1,
    }

    assert response_dict == response_expected


def test_accounts_post(client, auth):
    """
    Test if permissionId can be set from -1 to 3 in the account
    created in the previous test
    """
    auth.login()

    response = client.post("/accounts/account?id=11&email=b@b.ch&permId=3")

    response_dict: dict = json.loads(response.data.decode("utf-8"))
    response_expected: dict = {"update_successful": True}

    assert response_dict == response_expected


def test_accounts_delete(client, auth):
    """
    Test if the account can be deleted again
    """
    auth.login()

    response = client.delete("/accounts/account?id=11")

    response_dict: dict = json.loads(response.data.decode("utf-8"))
    response_expected: dict = {"delete_successful": True}

    assert response_dict == response_expected
