from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from .base import BaseSchema


# 基础 Schema
class ShopBase(BaseSchema):
    id: int
    name: str
    address: str
    phone: Optional[str] = None
    open_time: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    cover_url: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    is_active: bool = True
    sort_order: int = 0


# 创建请求 Schema
class ShopCreate(ShopBase):
    pass


# 更新请求 Schema
class ShopUpdate(BaseSchema):
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    open_time: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    cover_url: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    is_active: Optional[bool] = None
    sort_order: Optional[int] = None


# 响应 Schema
class ShopResponse(ShopBase):
    pass


class ShopListResponse(BaseModel):
    items: list[ShopResponse]
