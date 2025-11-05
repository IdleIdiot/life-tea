from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.auth import get_db_dep, get_current_user_dep
from app.schemas.response import success_response

router = APIRouter()


@router.get("/orders")
async def get_user_orders(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user_dep),
):
    """获取用户订单列表（简化版本）"""
    try:
        # 这里暂时返回空列表，实际应该查询数据库
        return success_response(data=[])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
