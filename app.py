from typing import Optional

from flask import Flask, request, make_response, Response

import handlers
from logging.config import dictConfig

from database import database
from database.models import MAX_URL_LENGTH

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "loggers": {
            "handlers": {
                "handlers": ["wsgi"],
                "level": "INFO",
                "propagate": False,
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

app = Flask(__name__)


@app.route("/v1/<short_url>")
def redirect_short_url(short_url=None):
    app.logger.info(f"redirecting short_url={short_url}")
    return handlers.redirect_short_url(short_url=short_url)


@app.post("/v1/shorten")
def shorten_url() -> Response:
    data = request.json
    url: str = data.get("url", None)
    if url is None:
        return make_response("missing url", 400)
    custom_short_url: str = data.get("custom_short_url", None)
    if not valid_input(url) or not valid_input(custom_short_url):
        return make_response(f"url too long, max url length is {MAX_URL_LENGTH}", 400)
    if custom_short_url is not None:
        return handlers.create_custom_short_url(
            url=url, custom_short_url=custom_short_url
        )
    return handlers.create_short_url(url=url)


def valid_input(url: Optional[str]) -> bool:
    return url is not None and len(url) <= MAX_URL_LENGTH


@app.teardown_appcontext
def shutdown_session(exceptions=None):
    database.remove_session()
