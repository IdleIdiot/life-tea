from sqlalchemy import (
    Column,
    String,
    Integer,
)
from .base import BaseModel


class Banner(BaseModel):
    __tablename__ = "banners"

    title = Column(String(64), nullable=True, comment="横幅标题")
    subtitle = Column(String(64), nullable=True, comment="横幅子标题")
    image_url = Column(String(200), nullable=True, comment="引用图片链接")
