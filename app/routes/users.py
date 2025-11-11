import logging
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from ..crud import user_crud
from ..dependencies import get_current_user, get_db
from ..schemas import ResponseModel, UserUpdate, success_response

logger = logging.getLogger(__name__)


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
        logger.info(f"新用户数据为：{profile_data.model_dump()}")
        logger.info(f"当前用户为：{current_user}")

        updated_user = user_crud.update_user(
            db,
            user_id=current_user["id"],
            update_data=profile_data.model_dump(),
        )
        logger.info("数据库更新成功")
        return success_response(data=updated_user.to_dict(), message="资料更新成功")
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/profile")
async def delete_user_profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    try:
        success = user_crud.delete(
            db=db,
            id=current_user["id"],
        )
        if success:
            return success_response(message="用户删除成功")
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
            cloud_env = "cloud://cloud1-7g2z6qs0ef1cb4ae.636c-cloud1-7g2z6qs0ef1cb4ae-1384302075"

            user_data = {
                "openid": openid,
                "unionid": unionid,
                "nick_name": f"用户{openid[-6:]}",
                "avatar_url": f"{cloud_env}/mikltea/data/images/user_avatar.png",
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
