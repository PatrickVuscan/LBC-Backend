"""Database models."""

import datetime
from sqlalchemy import Boolean, Column, Integer, String, Numeric, DateTime
from api.database.db_initialize import Base


class User(Base):
    """SQL User Model."""

    __tablename__ = "USERS"

    username = Column(String, unique=True, primary_key=True)
    password = Column(String, nullable=False)  # Not enforcing char limit because hash coded data may be long

    name = Column(String)
    age = Column(Integer)
    email = Column(String)


class UserPosts(Base):
    "SQL Post Model."
    __tablename__ = "USER_POSTS"

    post_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String)
    anonymous = Column(Boolean, unique=False, default=False)
    date_time = Column(DateTime, nullable=False)
    topic = Column(String(255))
    post_header = Column(String)
    post_body = Column(String)


class Comment(Base):
    "SQL Comment Model."
    __tablename__ = "COMMENTS"

    comment_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    post_id = Column(Integer)  # post_id of USER_POSTS that this comment is a part of
    user_id = Column(Integer)  # user_id of USER that posted the comment
    content = Column(String)
    date_time = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)  # Date Time posted


class EmergencyContacts(Base):
    """SQL Contact Model."""

    __tablename__ = "EMERGENCY_CONTACTS"

    emergency_contact_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    topic = Column(String(255))
    phone = Column(String(32))
    email = Column(String(255))
    longitude = Column(Numeric(4, 8))
    latitude = Column(Numeric(4, 8))  # 4 digit before decimal (not sure if negative sign takes a digit)
