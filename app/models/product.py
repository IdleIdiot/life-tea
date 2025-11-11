from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Numeric,
    Boolean,
    JSON,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from .base import BaseModel


class Product(BaseModel):
    __tablename__ = "products"

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
        nullable=False,
        comment="外键，关联 categories.id",
    )
    name = Column(String(100), nullable=False, comment="商品名称（如：珍珠奶茶）")
    description = Column(Text, nullable=True, comment="商品描述")
    main_image = Column(String(255), nullable=False, comment="主图URL")
    image_list = Column(JSON, nullable=True, comment="轮播图URL数组")
    base_price = Column(Numeric(10, 2), nullable=False, comment="基础价格（小杯价格）")
    is_hot = Column(Boolean, default=False, comment="是否热门推荐")
    is_new = Column(Boolean, default=False, comment="是否新品")
    sales_volume = Column(Integer, default=0, comment="总销量")
    month_sales = Column(Integer, default=0, comment="月销量")
    stock = Column(Integer, default=999, comment="库存（-1表示无限）")
    status = Column(Boolean, default=True, comment="状态 (True:上架, False:下架)")
    sort_order = Column(Integer, default=0, comment="排序")

    # 关系定义
    category = relationship("Category", back_populates="products")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.base_price})>"
