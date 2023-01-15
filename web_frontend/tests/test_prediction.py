import pytest
from frontend.db import get_db

def test_index(client, auth):
    """Tests redirection if not logged and Home page display if logged in."""
    response = client.get('/')
    assert response.headers["Location"] == "/auth/login"

    auth.login()
    response = client.get('/')
    assert b'Logout' in response.data
    assert b'Hauspreise' in response.data
    assert b'Postleitzahl' in response.data
    assert b'Anzahl Zimmer' in response.data
    assert b'form method="post"' in response.data