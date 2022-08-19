import uuid

from sqlalchemy import Column, String

from database import Base


class Url(Base):
    __tablename__ = 'urls'
    id = Column(String(36), primary_key=True, unique=True)
    short_url = Column(String(2048), primary_key=True, unique=True)
    original_url = Column(String(2048), nullable=False)

    def __init__(self, short_url=None, original_url=None):
        self.id = str(uuid.uuid4())
        self.short_url = short_url
        self.original_url = original_url

    def __repr__(self):
        return '<Url original_url=%r short_url=%r>' % (self.original_url, self.short_url)
