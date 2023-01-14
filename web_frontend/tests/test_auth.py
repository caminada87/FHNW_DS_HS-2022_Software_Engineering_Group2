import pytest
from flask import g, session
from frontend.db import get_db


def test_register(client, app):
    """tests a successful registration
    """
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'email': 'a@a.ch', 'password': 'a'}
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert get_db().execute(
            "SELECT * FROM user WHERE email = 'a@a.ch'",
        ).fetchone() is not None


@pytest.mark.parametrize(('email', 'password', 'message'), (
    ('', '', b'Die Email Adresse muss angegeben werden.'),
    ('a@a.ch', '', b'Bitte ein Passwort eingeben.'),
    ('test@tester.com', '1234', b'Die Email test@tester.com ist bereits registriert.'),
))
def test_register_validate_input(client, email, password, message):
    """Tests all possible failed results in the registration process
    """
    response = client.post(
        '/auth/register',
        data={'email': email, 'password': password}
    )
    assert message in response.data


def test_logout(client, auth):
    """Tests the logout functionality
    """
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session