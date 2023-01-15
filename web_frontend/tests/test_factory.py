from frontend import create_app


def test_config() -> None:
    """
    Test creation of the web app.
    """
    assert not create_app().testing
    assert create_app({"TESTING": True}).testing


def test_hello(client) -> None:
    """
    Test the hello world answer from web app.
    """
    response = client.get("/hello")
    assert response.data == b"<p>Hello, World!</p>"
