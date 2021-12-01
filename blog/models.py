import uuid

from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from database import Base


class Blog(Base):
    __tablename__ = 'blog'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title = Column(String,)
    body = Column(String,)
    published = Column(Boolean,)
    user_id = Column(UUID, ForeignKey('user.id'))
    owner = relationship('User', back_populates='blogs')
