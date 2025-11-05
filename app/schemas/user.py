from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import date
from app.schemas.base import BaseSchema


class UserBase(BaseSchema):
    """用户基础模型"""

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


class UserUpdate(BaseModel):
    """更新用户请求模型"""

    nick_name: Optional[str] = Field(None, max_length=100, description="昵称")
    avatar_url: Optional[str] = Field(None, max_length=255, description="头像URL")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    gender: Optional[int] = Field(None, ge=0, le=2, description="性别")
    birthday: Optional[date] = Field(None, description="生日")
    member_level: Optional[int] = Field(None, ge=1, description="会员等级")


class UserResponse(UserBase):
    """用户响应模型"""

    id: int

    class Config:
        from_attributes = True


class UserAddressBase(BaseSchema):
    """用户地址基础模型"""

    contact_name: str = Field(
        ..., min_length=1, max_length=50, description="收货人姓名"
    )
    contact_phone: str = Field(
        ..., min_length=11, max_length=20, description="收货人电话"
    )
    region: str = Field(..., min_length=1, max_length=255, description="省市区")
    address_detail: str = Field(
        ..., min_length=1, max_length=255, description="详细地址"
    )
    latitude: Optional[str] = Field(None, description="纬度")
    longitude: Optional[str] = Field(None, description="经度")
    is_default: bool = Field(default=False, description="是否默认地址")


class UserAddressCreate(UserAddressBase):
    """创建地址请求模型"""

    user_id: int = Field(..., description="用户ID")


class UserAddressUpdate(BaseModel):
    """更新地址请求模型"""

    contact_name: Optional[str] = Field(
        None, min_length=1, max_length=50, description="收货人姓名"
    )
    contact_phone: Optional[str] = Field(
        None, min_length=11, max_length=20, description="收货人电话"
    )
    region: Optional[str] = Field(
        None, min_length=1, max_length=255, description="省市区"
    )
    address_detail: Optional[str] = Field(
        None, min_length=1, max_length=255, description="详细地址"
    )
    latitude: Optional[str] = Field(None, description="纬度")
    longitude: Optional[str] = Field(None, description="经度")
    is_default: Optional[bool] = Field(None, description="是否默认地址")


class UserAddressResponse(UserAddressBase):
    """地址响应模型"""

    id: int
    user_id: int

    class Config:
        from_attributes = True


class UserWithAddresses(UserResponse):
    """用户信息（包含地址列表）"""

    addresses: List[UserAddressResponse] = []


class UserLoginRequest(BaseModel):
    """用户登录请求"""

    code: str = Field(..., description="微信登录code")


class UserLoginResponse(BaseModel):
    """用户登录响应"""

    user: UserResponse
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class UserProfileUpdate(BaseModel):
    """用户资料更新请求"""

    nick_name: Optional[str] = Field(None, max_length=100, description="昵称")
    avatar_url: Optional[str] = Field(None, max_length=255, description="头像URL")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    gender: Optional[int] = Field(None, ge=0, le=2, description="性别")
    birthday: Optional[date] = Field(None, description="生日")


__all__ = [
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserAddressBase",
    "UserAddressCreate",
    "UserAddressUpdate",
    "UserAddressResponse",
    "UserWithAddresses",
    "UserLoginRequest",
    "UserLoginResponse",
    "UserProfileUpdate",
]
