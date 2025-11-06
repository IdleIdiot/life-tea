from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas.response import success_response
from app.crud import user_crud

router = APIRouter()


@router.get("/profile")
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """获取用户资料"""
    return success_response(data=current_user)


@router.put("/profile")
async def update_user_profile(
    profile_data: dict,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
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
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
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
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
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


@router.get("/me")
async def get_current_user(current_user: dict = Depends(get_current_user)):
    """获取当前用户信息（简化版本）"""
    return success_response(data=current_user)


@router.post("/register")
async def wechat_register(req: Request, db: Session = Depends(get_db)):
    """微信小程序登录"""
    try:
        # 获取 openid
        openid = req.headers.get("x-wx-openid", None)
        unionid = req.headers.get("x-wx-unionid", "")

        if not openid:
            raise HTTPException(status_code=400, detail="获取openid失败")

        # 查找或创建用户
        db_user = user_crud.get_by_openid(db, openid=openid)
        if not db_user:
            # 创建新用户
            user_data = {
                "openid": openid,
                "unionid": unionid,
                "nick_name": f"用户{openid[-6:]}",
                "avatar_url": "cloud://cloud1-7g2z6qs0ef1cb4ae.636c-cloud1-7g2z6qs0ef1cb4ae-1384302075/mikltea/data/images/user_avatar.png",
                "phone": "",
                "gender": 0,
                "member_level": 1,
                "points": 0,
                "status": 1,
            }
            db_user = user_crud.create_user(db, user_data=user_data)

        user_response = {
            "id": db_user.id,
            "openid": db_user.openid,
            "nick_name": db_user.nick_name,
            "avatar_url": db_user.avatar_url,
            "phone": db_user.phone,
            "gender": db_user.gender,
            "member_level": db_user.member_level,
            "points": db_user.points,
            "status": db_user.status,
        }

        return success_response(
            data={
                "user": user_response,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
