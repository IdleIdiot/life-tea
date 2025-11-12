from typing import List, Optional

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..crud import shop_crud
from ..dependencies import get_db
from ..schemas import (
    ResponseModel,
    ShopCreate,
    ShopListResponse,
    ShopResponse,
    ShopUpdate,
    error_response,
    not_found_response,
    success_response,
)

router = APIRouter()


@router.get("/shops", response_model=ResponseModel[ShopListResponse])
async def get_shops(
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db),
):
    """获取店铺列表"""
    try:
        shops = shop_crud.get_all(db)
        data = ShopListResponse(shops)
        return success_response(data=data, message="获取店铺列表成功")
    except Exception as e:
        return error_response(message="获取店铺列表失败", error_detail=str(e))


@router.get("/current", response_model=ResponseModel[ShopResponse])
async def get_current_shop(db: Session = Depends(get_db)):
    """获取当前营业的店铺"""
    try:
        shop = shop_crud.get_active_shop(db)
        if not shop:
            return not_found_response(message="未找到营业中的店铺")
        return success_response(data=shop, message="获取店铺信息成功")
    except Exception as e:
        return error_response(message="获取店铺信息失败", error_detail=str(e))
