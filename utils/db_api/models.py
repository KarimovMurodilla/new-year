from distutils.sysconfig import get_makefile_filename
from sqlalchemy import Column, BigInteger, Integer, String, DateTime, Boolean
from sqlalchemy.sql import func
from utils.db_api.base import Base


class Users(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True, unique=True, autoincrement=False)
    username = Column(String(20))
    phone_number = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Concats(Base):
    __tablename__ = "concats"

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    name = Column(String(50))
    gender = Column(String(10))
    age = Column(Integer())
    hobbies = Column(String(50))
    wishes = Column(String(50))
    type = Column(String(15))
    file_id = Column(String(150))
    bot_name = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Promocodes(Base):
    __tablename__ = "promocodes"

    id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), nullable=True)
    code = Column(String(50))
    status = Column(Boolean, default=False)
