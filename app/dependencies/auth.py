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
    return {
        "id": user.id,
        "openid": user.openid,
        "unionid": user.unionid,
        "nick_name": user.nick_name,
        "avatar_url": user.avatar_url,
        "phone": getattr(user, "phone", ""),
        "gender": getattr(user, "gender", 0),
        "birthday": getattr(user, "birthday", "2025-01-01"),
        "member_level": getattr(user, "member_level", 1),
        "points": getattr(user, "points", 0),
        "status": getattr(user, "status", 1),
    }
