import uuid

from sqlalchemy import Column, String

from database import Base

MAX_URL_LENGTH: int = 2048


class Url(Base):
    __tablename__ = "urls"
    id = Column(String(36), primary_key=True, unique=True)
    short_url = Column(String(MAX_URL_LENGTH), primary_key=True, unique=True)
    original_url = Column(String(MAX_URL_LENGTH), nullable=False)

    def __init__(self, short_url=None, original_url=None):
        self.id = str(uuid.uuid4())
        self.short_url = short_url
        self.original_url = original_url
