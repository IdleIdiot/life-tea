from typing import List, Optional

from pydantic import BaseModel

from .base import BaseSchema
from .product import ProductResponse  # 导入ProductResponse


class CategoryBase(BaseSchema):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    sort_order: int = 0
    status: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseSchema):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    sort_order: int = 0
    status: bool = True
    pass


class CategoryResponse(CategoryBase):
    products: List[ProductResponse] = []  # 添加产品列表字段


# 列表响应 Schema
class CategoryListResponse(BaseModel):
    items: list[CategoryResponse]
