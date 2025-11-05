from sqlalchemy import Column, String, Integer, Boolean, Text, Numeric, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class Category(BaseModel):
    __tablename__ = "categories"

    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    image_url = Column(String(255), nullable=True)
    sort_order = Column(Integer, default=0)
    status = Column(Integer, default=1)  # 1:显示, 0:隐藏

    products = relationship("Product", back_populates="category")


class Product(BaseModel):
    __tablename__ = "products"

    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    main_image = Column(String(255), nullable=False)
    image_list = Column(JSON, nullable=True)
    base_price = Column(Numeric(10, 2), nullable=False)
    is_hot = Column(Boolean, default=False)
    is_new = Column(Boolean, default=False)
    sales_volume = Column(Integer, default=0)
    month_sales = Column(Integer, default=0)
    stock = Column(Integer, default=999)  # -1表示无限
    status = Column(Integer, default=1)  # 1:上架, 0:下架
    sort_order = Column(Integer, default=0)

    category = relationship("Category", back_populates="products")
    specs = relationship("ProductSpec", back_populates="product")


class ProductSpec(BaseModel):
    __tablename__ = "product_specs"

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    spec_type = Column(Integer, nullable=False)  # 1:杯型, 2:温度, 3:甜度, 4:加料
    spec_name = Column(String(50), nullable=False)
    additional_price = Column(Numeric(8, 2), default=0.00)
    stock = Column(Integer, default=999)  # -1表示无限
    is_default = Column(Boolean, default=False)
    status = Column(Integer, default=1)  # 1:可用, 0:不可用
    sort_order = Column(Integer, default=0)

    product = relationship("Product", back_populates="specs")


class Favorite(BaseModel):
    __tablename__ = "favorites"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
