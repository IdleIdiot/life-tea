from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, Optional

from pydantic import BaseModel

from .base import BaseSchema


class ProductBase(BaseSchema):
    category_id: int
    name: str
    description: Optional[str] = None
    main_image: str
    image_list: Optional[Dict[str, Any]] = None
    base_price: Decimal
    is_hot: bool = False
    is_new: bool = False
    sales_volume: int = 0
    month_sales: int = 0
    stock: int = 999
    status: bool = True
    sort_order: int = 0
    created_at: datetime
    updated_at: datetime


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseSchema):
    category_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    main_image: Optional[str] = None
    image_list: Optional[Dict[str, Any]] = None
    base_price: Optional[Decimal] = None
    is_hot: Optional[bool] = None
    is_new: Optional[bool] = None
    stock: Optional[int] = None
    status: Optional[bool] = None
    sort_order: Optional[int] = None


class ProductResponse(ProductBase):
    pass


# 列表响应 Schema
class ProductListResponse(BaseModel):
    items: list[ProductResponse]
