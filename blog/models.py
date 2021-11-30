import uuid

from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

from database import Base


class Blog(Base):
    __tablename__ = 'blog'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String,)
    body = Column(String,)
    published = Column(Boolean,)


class User(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String,)
    email = Column(String,)
    password = Column(String,)
