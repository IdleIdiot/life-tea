from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies.auth import get_db_dep, get_current_user_dep
from app.schemas.response import success_response
from app.crud.user import user as user_crud, user_address as address_crud

router = APIRouter()


@router.get("/profile")
async def get_user_profile(current_user: dict = Depends(get_current_user_dep)):
    """获取用户资料"""
    return success_response(data=current_user)


@router.put("/profile")
async def update_user_profile(
    profile_data: dict,
    db: Session = Depends(get_db_dep),
    current_user: dict = Depends(get_current_user_dep),
):
    """更新用户资料"""
    try:
        updated_user = user_crud.update_user(
            db, user_id=current_user["id"], user_in=profile_data
        )

        user_response = {
            "id": updated_user.id,
            "openid": updated_user.openid,
            "nick_name": updated_user.nick_name,
            "avatar_url": updated_user.avatar_url,
            "phone": updated_user.phone,
            "gender": updated_user.gender,
            "member_level": updated_user.member_level,
            "points": updated_user.points,
            "status": updated_user.status,
        }

        return success_response(data=user_response, message="资料更新成功")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/addresses")
async def get_user_addresses(
    db: Session = Depends(get_db_dep),
    current_user: dict = Depends(get_current_user_dep),
):
    """获取用户地址列表"""
    try:
        addresses = address_crud.get_by_user(db, user_id=current_user["id"])

        address_list = []
        for addr in addresses:
            address_list.append(
                {
                    "id": addr.id,
                    "contact_name": addr.contact_name,
                    "contact_phone": addr.contact_phone,
                    "region": addr.region,
                    "address_detail": addr.address_detail,
                    "latitude": addr.latitude,
                    "longitude": addr.longitude,
                    "is_default": addr.is_default,
                }
            )

        return success_response(data=address_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/addresses")
async def create_user_address(
    address_data: dict,
    db: Session = Depends(get_db_dep),
    current_user: dict = Depends(get_current_user_dep),
):
    """创建用户地址"""
    try:
        address_data["user_id"] = current_user["id"]
        address = address_crud.create(db, obj_in=address_data)

        return success_response(
            data={
                "id": address.id,
                "contact_name": address.contact_name,
                "contact_phone": address.contact_phone,
                "region": address.region,
                "address_detail": address.address_detail,
                "latitude": address.latitude,
                "longitude": address.longitude,
                "is_default": address.is_default,
            },
            message="地址创建成功",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
