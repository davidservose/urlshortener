import http
from unittest.mock import MagicMock, patch

import pytest
from flask import Response

import handlers
from database.models import Url
import app

test_original_url = "http://www.testoriginalurl.com"
test_short_url = "test_shot_url"


app_context = app.app.app_context()
app_context.push()


@patch('database.database.get_url_record')
def test_redirect_short_url(get_url_record: MagicMock):
    get_url_record.return_value = Url(short_url=test_short_url, original_url=test_original_url)
    response: Response = handlers.redirect_short_url(short_url=test_short_url)
    assert response
    assert response.status_code == http.HTTPStatus.FOUND
    assert response.location == test_original_url


@patch('database.database.get_url_record')
def test_redirect_short_url_not_found(get_url_record: MagicMock):
    get_url_record.return_value = None
    response: Response = handlers.redirect_short_url(short_url=test_short_url)
    assert response
    assert response.status_code == http.HTTPStatus.NOT_FOUND


