import app
from database.models import MAX_URL_LENGTH


def test_valid_input():
    assert app.valid_input(None)
    assert app.valid_input("valid")
    assert not app.valid_input("1" * MAX_URL_LENGTH + "1")
