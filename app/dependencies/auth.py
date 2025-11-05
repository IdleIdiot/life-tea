from fastapi import Depends, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.dependencies.database import get_db
from app.services.auth import auth_service
from app.crud.user import user_crud

# JWT Bearer 认证
security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> dict:
    """
    简化版：获取当前认证用户（一步完成）
    """
    # 1. 检查 Token 是否存在
    if not credentials or credentials.scheme != "Bearer":
        raise HTTPException(status_code=401, detail="请提供有效的Bearer Token")

    token = credentials.credentials

    # 2. 验证 Token
    payload = auth_service.verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token无效或已过期")

    # 3. 获取用户ID
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="无效的Token载荷")

    # 4. 查询用户（同步方式，适合mysqlclient）
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")

    if getattr(user, "status", 1) == 0:  # 兼容没有status字段的情况
        raise HTTPException(status_code=403, detail="用户已被禁用")

    # 5. 返回用户信息
    return {
        "id": user.id,
        "openid": user.openid,
        "nick_name": user.nick_name,
        "avatar_url": user.avatar_url,
        "phone": getattr(user, "phone", ""),
        "gender": getattr(user, "gender", 0),
        "member_level": getattr(user, "member_level", 1),
        "points": getattr(user, "points", 0),
        "status": getattr(user, "status", 1),
    }


async def verify_token_only(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """只验证Token，不查询用户信息"""
    if not credentials or credentials.scheme != "Bearer":
        raise HTTPException(status_code=401, detail="请提供有效的Bearer Token")

    payload = auth_service.verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Token无效或已过期")

    return payload


# 依赖注入简化
CurrentUser = Depends(get_current_user)
ValidToken = Depends(verify_token_only)
