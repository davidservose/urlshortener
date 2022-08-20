import logging

from flask import Response, make_response, redirect

from database.models import Url
from database import database
from hashing import Hasher

logger = logging.getLogger(__name__)


def redirect_short_url(short_url: str) -> Response:
    url_record: Url = database.get_url_record(short_url=short_url)
    if url_record is None:
        logger.info(f"No record found for shorturl={short_url}")
        return make_response("short url not found", 404)
    logger.info(
        f"redirecting short_url={url_record.short_url} to original_url={url_record.original_url}"
    )
    return redirect(url_record.original_url)


def create_custom_short_url(url: str, custom_short_url: str) -> Response:
    if database.get_url_record(short_url=custom_short_url) is not None:
        return make_response("custom_short_url already exists", 400)
    database.create_url_record(original_url=url, short_url=custom_short_url)
    return make_response(custom_short_url, 201)


def create_short_url(url: str) -> Response:
    hashed_url = Hasher.hash(value=url)
    short_url: str = str(hashed_url)
    while database.get_url_record(short_url=short_url) is not None:
        logger.info("found existing short url, finding unused hash")
        hashed_url += 1
        short_url = str(hashed_url)
    logger.info(f"url={url}, short_url={short_url}")
    database.create_url_record(original_url=url, short_url=short_url)
    return make_response(short_url, 201)
