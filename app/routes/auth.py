from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.response import success_response
from app.services.auth import auth_service
from app.services.wechat import wechat_service
from app.crud.user import user_crud

router = APIRouter()


@router.post("/login")
async def wechat_login(code: str, db: Session = Depends(get_db)):
    """微信小程序登录"""
    try:
        # 获取 openid
        wechat_data = await wechat_service.code2session(code)

        if "errcode" in wechat_data:
            raise HTTPException(
                status_code=400, detail=f"微信登录失败: {wechat_data.get('errmsg')}"
            )

        openid = wechat_data.get("openid")
        if not openid:
            raise HTTPException(status_code=400, detail="获取openid失败")

        # 查找或创建用户
        db_user = user_crud.get_by_openid(db, openid=openid)
        if not db_user:
            # 创建新用户
            user_data = {
                "openid": openid,
                "unionid": wechat_data.get("unionid"),
                "nick_name": f"用户{openid[-6:]}",
                "avatar_url": "cloud://cloud1-7g2z6qs0ef1cb4ae.636c-cloud1-7g2z6qs0ef1cb4ae-1384302075/mikltea/data/images/user_avatar.png",
                "phone": "",
                "gender": 0,
                "member_level": 1,
                "points": 0,
                "status": 1,
            }
            db_user = user_crud.create_user(db, user_data=user_data)

        # 生成 JWT token
        access_token = auth_service.create_access_token(data={"sub": str(db_user.id)})

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
                "access_token": access_token,
                "token_type": "bearer",
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
