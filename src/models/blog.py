from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..utils.database import Base

func: callable


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True)
    slug = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(String, nullable=False)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    datetime_created = Column(DateTime, default=func.now())
    datetime_updated = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=False)

    author = relationship("User", back_populates="blogs")
