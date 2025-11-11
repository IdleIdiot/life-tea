from pydantic import BaseModel
from typing import Optional
from .base import BaseSchema


class CategoryBase(BaseSchema):
    name: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    sort_order: int = 0
    status: bool = True


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseSchema):
    name: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    sort_order: Optional[int] = None
    status: Optional[bool] = None


class CategoryResponse(CategoryBase):
    pass


# 列表响应 Schema
class CategoryListResponse(BaseModel):
    items: list[CategoryResponse]
