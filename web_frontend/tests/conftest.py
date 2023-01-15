import os
import tempfile
import pytest

from frontend import create_app
from frontend.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
    _data_sql = f.read().decode("utf8")


@pytest.fixture
def app() -> None:
    """
    Create test web app.
    """
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(
        {
            "TESTING": True,
            "BASE_URL": "http://localhost:5000",
            "DATABASE": db_path,
        }
    )

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app) -> None:
    """
    Run test_client on app.
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """
    Test runner.
    """
    return app.test_cli_runner()


class AuthActions(object):
    """
    The user has to be logged in most of the time. Also, during testing.
    """

    def __init__(self, client):
        self._client = client

    def login(self, email="test@tester.com", password="1234") -> None:
        """
        Login with test user.
        @param email: test user e-mail
        @param password: test user password
        """
        return self._client.post(
            "/auth/login", data={"email": email, "password": password}
        )

    def logout(self) -> None:
        """
        User logout.
        """
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client) -> AuthActions:
    """
    Test authentication.
    """
    return AuthActions(client)
