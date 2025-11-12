from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session

from ..crud.user import user_crud
from ..models import User
from .database import get_db


async def get_current_user(
    req: Request,
    db: Session = Depends(get_db),
) -> User:
    """
    简化版：获取当前认证用户（一步完成）
    """
    user = user_crud.get_by_openid(db, openid=req.headers.get("x-wx-openid"))

    if not user:
        raise HTTPException(status_code=401, detail="未授权用户,请先注册")

    if getattr(user, "status", 1) == 0:  # 兼容没有status字段的情况
        raise HTTPException(status_code=403, detail="用户已被禁用")

    # 5. 返回用户信息
    return user
