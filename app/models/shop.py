from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from .base import BaseModel


class Shop(BaseModel):
    __tablename__ = "shops"

    name = Column(String(100), nullable=False, comment="店铺名称")
    address = Column(String(200), nullable=False, comment="详细地址")
    phone = Column(String(20), nullable=True, comment="联系电话")
    open_time = Column(String(50), nullable=True, comment="营业时间")
    description = Column(Text, nullable=True, comment="店铺描述")
    logo_url = Column(String(200), nullable=True, comment="店铺Logo")
    cover_url = Column(String(200), nullable=True, comment="封面图片")
    latitude = Column(String(20), nullable=True, comment="纬度")
    longitude = Column(String(20), nullable=True, comment="经度")
    is_active = Column(Boolean, default=True, comment="是否营业")
    sort_order = Column(Integer, default=0, comment="排序权重")

    def __repr__(self):
        return f"<Shop {self.name}>"
