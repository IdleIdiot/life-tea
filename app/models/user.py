from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    openid = Column(String(64), unique=True, index=True, nullable=False)
    unionid = Column(String(64), unique=True, index=True, nullable=True)
    nick_name = Column(String(100), nullable=True)
    avatar_url = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True, index=True)
    gender = Column(Integer, default=0)  # 0:未知, 1:男, 2:女
    birthday = Column(Date, nullable=True)
    member_level = Column(Integer, default=1)  # 1:普通, 2:VIP, 3:SVIP
    points = Column(Integer, default=0)
    status = Column(Integer, default=1)  # 1:正常, 0:禁用


class UserAddress(BaseModel):
    __tablename__ = "user_addresses"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    contact_name = Column(String(50), nullable=False)
    contact_phone = Column(String(20), nullable=False)
    region = Column(String(255), nullable=False)
    address_detail = Column(String(255), nullable=False)
    latitude = Column(String(20), nullable=True)
    longitude = Column(String(20), nullable=True)
    is_default = Column(Boolean, default=False)
