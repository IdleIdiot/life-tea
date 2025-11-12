from typing import Optional

from pydantic import BaseModel

from .base import BaseSchema


class BannerBase(BaseSchema):
    id: Optional[int] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    image_url: Optional[str] = None


# 请求 Schema
class BannerCreate(BannerBase):
    pass


class BannerUpdate(BaseSchema):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    image_url: Optional[str] = None


# 响应 Schema
class BannerResponse(BannerBase):
    pass


# 列表响应 Schema
class BannerListResponse(BaseModel):
    items: list[BannerResponse]
