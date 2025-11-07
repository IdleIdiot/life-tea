from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, Request

from app.crud.user import user_crud
from app.dependencies import get_db


async def get_current_user(
    req: Request,
    db: Session = Depends(get_db),
) -> dict:
    """
    简化版：获取当前认证用户（一步完成）
    """
    user = user_crud.get_by_openid(db, openid=req.headers.get("x-wx-openid"))
    if getattr(user, "status", 1) == 0:  # 兼容没有status字段的情况
        raise HTTPException(status_code=403, detail="用户已被禁用")

    # 5. 返回用户信息
    return user.to_dict()
