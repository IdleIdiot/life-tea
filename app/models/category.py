from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
)
from sqlalchemy.orm import relationship

from .base import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"

    name = Column(String(50), nullable=False, comment="分类名称")
    description = Column(String(255), nullable=True, comment="分类描述")
    image_url = Column(String(255), nullable=True, comment="分类图片")
    sort_order = Column(Integer, default=0, comment="排序权重（数字越大越靠前）")
    status = Column(Boolean, default=True, comment="状态 (True:显示, False:隐藏)")

    # 与商品的关联关系
    products = relationship(
        "Product", back_populates="category", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"
