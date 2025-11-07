from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

T = TypeVar("T")


class ResponseCode(int, Enum):
    """响应状态码枚举"""

    SUCCESS = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    INTERNAL_ERROR = 500


class ResponseModel(BaseModel, Generic[T]):
    """标准响应模型"""

    code: int = Field(default=ResponseCode.SUCCESS, description="状态码")
    message: str = Field(default="success", description="响应消息")
    data: Optional[T] = Field(default=None, description="响应数据")
    timestamp: datetime = Field(default_factory=datetime.now, description="时间戳")

    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}


class ErrorResponse(BaseModel):
    """错误响应模型"""

    code: int = Field(..., description="错误码")
    message: str = Field(..., description="错误信息")
    detail: Optional[Any] = Field(default=None, description="错误详情")
    timestamp: datetime = Field(default_factory=datetime.now, description="时间戳")

    class Config:
        json_encoders = {datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")}


# 响应工具函数
def success_response(data: Any = None, message: str = "success") -> ResponseModel:
    """成功响应"""
    return ResponseModel(code=ResponseCode.SUCCESS, message=message, data=data)


def error_response(
    code: int = ResponseCode.INTERNAL_ERROR,
    message: str = "服务器内部错误",
    detail: Any = None,
) -> ErrorResponse:
    """错误响应"""
    return ErrorResponse(code=code, message=message, detail=detail)


def not_found_response(message: str = "资源不存在") -> ErrorResponse:
    """404 响应"""
    return error_response(code=ResponseCode.NOT_FOUND, message=message)


def unauthorized_response(message: str = "未授权访问") -> ErrorResponse:
    """401 响应"""
    return error_response(code=ResponseCode.UNAUTHORIZED, message=message)


def forbidden_response(message: str = "禁止访问") -> ErrorResponse:
    """403 响应"""
    return error_response(code=ResponseCode.FORBIDDEN, message=message)


def bad_request_response(
    message: str = "请求参数错误", detail: Any = None
) -> ErrorResponse:
    """400 响应"""
    return error_response(code=ResponseCode.BAD_REQUEST, message=message, detail=detail)
