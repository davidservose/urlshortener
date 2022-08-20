import http
from unittest.mock import MagicMock, patch
from flask import Response

import handlers
from database.models import Url
import app

test_original_url: str = "http://www.testoriginalurl.com"
test_short_url: str = "test_shot_url"
hash_value: int = 100


app_context = app.app.app_context()
app_context.push()


@patch("database.database.get_url_record")
def test_redirect_short_url(get_url_record: MagicMock):
    get_url_record.return_value = Url(
        short_url=test_short_url, original_url=test_original_url
    )
    response: Response = handlers.redirect_short_url(short_url=test_short_url)
    assert response
    assert response.status_code == http.HTTPStatus.FOUND
    assert response.location == test_original_url


@patch("database.database.get_url_record")
def test_redirect_short_url_not_found(get_url_record: MagicMock):
    get_url_record.return_value = None
    response: Response = handlers.redirect_short_url(short_url=test_short_url)
    assert response
    assert response.status_code == http.HTTPStatus.NOT_FOUND


@patch("hashing.Hasher.hash")
@patch("database.database.get_url_record")
@patch("database.database.create_url_record")
def test_create_short_url(
    create_url_record: MagicMock, get_url_record: MagicMock, hash_function: MagicMock
):
    hash_function.return_value = hash_value
    get_url_record.return_value = None
    create_url_record.return_value = Url(
        short_url=test_short_url, original_url=test_original_url
    )
    response: Response = handlers.create_short_url(url=test_original_url)
    assert response
    assert response.status_code == http.HTTPStatus.CREATED
    assert response.data.decode("utf-8") == str(hash_value)


@patch("hashing.Hasher.hash")
@patch("database.database.get_url_record")
@patch("database.database.create_url_record")
def test_create_short_url_exists(
    create_url_record: MagicMock, get_url_record: MagicMock, hash_function: MagicMock
):
    hash_function.return_value = hash_value
    get_url_record.side_effect = [
        Url(short_url="not_test_short_url", original_url="not_test_original_url"),
        None,
    ]
    create_url_record.return_value = Url(
        short_url=test_short_url, original_url=test_original_url
    )
    response: Response = handlers.create_short_url(url=test_original_url)
    assert response
    assert response.status_code == http.HTTPStatus.CREATED
    assert response.data.decode("utf-8") != str(hash_value)


@patch("database.database.get_url_record")
@patch("database.database.create_url_record")
def test_create_custom_short_url(
    create_url_record: MagicMock, get_url_record: MagicMock
):
    get_url_record.return_value = None
    create_url_record.return_value = Url(
        short_url=test_short_url, original_url=test_original_url
    )
    response: Response = handlers.create_custom_short_url(
        url=test_original_url, custom_short_url=test_short_url
    )
    assert response
    assert response.status_code == http.HTTPStatus.CREATED
    assert response.data.decode("utf-8") == test_short_url


@patch("database.database.get_url_record")
def test_create_custom_short_url_exists(get_url_record: MagicMock):
    get_url_record.return_value = Url(
        short_url=test_short_url, original_url=test_original_url
    )
    response: Response = handlers.create_custom_short_url(
        url=test_original_url, custom_short_url=test_short_url
    )
    assert response
    assert response.status_code == http.HTTPStatus.BAD_REQUEST
