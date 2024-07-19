from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..utils.database import Base

func: callable


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    datetime_created = Column(DateTime, default=func.now())
    datetime_updated = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted = Column(Boolean, default=False)

    blogs = relationship("Blog", back_populates="author")
