from typing import Optional
from pydantic import Field, BaseModel
from datetime import date
from .base import BaseSchema


class UserBase(BaseSchema):
    """用户基础模型"""

    # TODO: 其他协议通过以下方式，完善字段检查和限制详细使用
    openid: str = Field(..., min_length=1, max_length=64, description="微信openid")
    unionid: Optional[str] = Field(None, max_length=64, description="微信unionid")
    nick_name: Optional[str] = Field(None, max_length=100, description="昵称")
    avatar_url: Optional[str] = Field(None, max_length=255, description="头像URL")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    gender: int = Field(default=0, ge=0, le=2, description="性别（0:未知,1:男,2:女）")
    birthday: Optional[date] = Field(None, description="生日")
    member_level: int = Field(default=1, ge=1, description="会员等级")
    points: int = Field(default=0, ge=0, description="积分")
    status: int = Field(default=1, description="状态（1:正常,0:禁用）")


class UserCreate(UserBase):
    """创建用户请求模型"""

    pass


class UserUpdate(BaseSchema):
    """更新用户请求模型"""

    nick_name: Optional[str] = Field(None, max_length=100, description="昵称")
    avatar_url: Optional[str] = Field(None, max_length=255, description="头像URL")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    gender: Optional[int] = Field(None, ge=0, le=2, description="性别")
    birthday: Optional[date] = Field(None, description="生日")
    # member_level: Optional[int] = Field(None, ge=1, description="会员等级")


class UserResponse(UserBase):
    pass


# 列表响应 Schema
class UserListResponse(BaseModel):
    items: list[UserResponse]
