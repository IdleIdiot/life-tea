from sqlalchemy.orm import Session

from app.models.user import User
from app.crud.base import CRUDBase


class UserCRUD(CRUDBase):
    """用户 CRUD 操作"""

    def __init__(self):
        super().__init__(User)

    def get_by_openid(self, db: Session, openid: str) -> User:
        """根据 openid 获取用户"""
        return db.query(self.model).filter(self.model.openid == openid).first()

    def get_by_phone(self, db: Session, phone: str):
        """根据手机号获取用户"""
        return db.query(self.model).filter(self.model.phone == phone).first()

    def create_user(self, db: Session, user_data: dict):
        """创建用户"""
        # 检查 openid 是否已存在
        if self.get_by_openid(db, user_data["openid"]):
            raise ValueError("用户已存在")

        user = self.model(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update_user(self, db: Session, user_id: int, update_data: dict):
        """更新用户信息"""
        user = self.get(db, user_id)
        if not user:
            raise ValueError("用户不存在")

        for field, value in update_data.items():
            if hasattr(user, field):
                setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user


# 创建实例
user_crud = UserCRUD()
