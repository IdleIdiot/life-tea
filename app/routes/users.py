from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.dependencies import get_db, get_current_user
from app.schemas import success_response, ResponseModel, ErrorResponse, UserUpdate
from app.crud import user_crud
from datetime import date

router = APIRouter()


@router.get("/profile")
async def get_user_profile(
    current_user: dict = Depends(get_current_user),
) -> ResponseModel:
    """获取用户资料"""
    return success_response(data=current_user)


@router.put("/profile")
async def update_user_profile(
    profile_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    """更新用户资料"""
    try:
        updated_user = user_crud.update_user(
            db,
            user_id=current_user["id"],
            user_data=profile_data,
        )
        return success_response(data=updated_user.to_dict(), message="资料更新成功")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
                "birthday": date.today(),
                "member_level": 1,
                "points": 0,
                "status": 1,
            }
            db_user = user_crud.create_user(db, user_data=user_data)

        return success_response(
            data=db_user.to_dict(),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
