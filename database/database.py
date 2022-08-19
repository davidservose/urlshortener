from database import db_session
from database.models import Url


def create_url_record(original_url: str, short_url: str) -> None:
    url_record = Url(original_url=original_url, short_url=short_url)
    db_session.add(url_record)
    db_session.commit()


def get_url_record(short_url: str) -> Url:
    return Url.query.filter(Url.short_url == short_url).first()


def remove_session() -> None:
    db_session.remove()
