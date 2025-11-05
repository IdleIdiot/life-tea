from fastapi import APIRouter, Depends, HTTPException
from app.schemas.response import success_response

router = APIRouter()


@router.get("/config")
async def get_wechat_config(url: str):
    """获取微信配置（简化版本）"""
    try:
        # 这里暂时返回空配置，实际应该实现微信JS-SDK配置
        return success_response(data={})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
