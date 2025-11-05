from sqlalchemy.orm import Session

from app.models.user import User, UserAddress


class UserCRUD:
    """用户 CRUD 操作"""

    def __init__(self):
        self.model = User

    def get_user(self, db: Session, user_id: int):
        """根据ID获取用户"""
        return db.query(self.model).filter(self.model.id == user_id).first()

    def get_by_openid(self, db: Session, openid: str):
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

    def update_points(self, db: Session, user_id: int, points: int):
        """更新用户积分"""
        user = self.get(db, user_id)
        if user:
            user.points = user.points + points if hasattr(user, "points") else points
            db.commit()
            db.refresh(user)
        return user


class UserAddressCRUD:
    """用户地址 CRUD 操作"""

    def __init__(self):
        self.model = UserAddress

    def get_user_address(self, db: Session, address_id: int):
        """根据ID获取地址"""
        return db.query(self.model).filter(self.model.id == address_id).first()

    def get_address_by_user(self, db: Session, user_id: int):
        """获取用户的所有地址"""
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id)
            .order_by(self.model.is_default.desc())
            .all()
        )

    def get_default_address(self, db: Session, user_id: int):
        """获取用户的默认地址"""
        return (
            db.query(self.model)
            .filter(self.model.user_id == user_id, self.model.is_default == True)
            .first()
        )

    def create_user_address(self, db: Session, address_data: dict):
        """创建地址"""
        address = self.model(**address_data)
        db.add(address)
        db.commit()
        db.refresh(address)
        return address

    def update_user_address(self, db: Session, address_id: int, update_data: dict):
        """更新地址"""
        address = self.get(db, address_id)
        if not address:
            raise ValueError("地址不存在")

        for field, value in update_data.items():
            if hasattr(address, field):
                setattr(address, field, value)

        db.commit()
        db.refresh(address)
        return address

    def set_default_address(self, db: Session, address_id: int, user_id: int):
        """设置默认地址"""
        # 取消所有默认地址
        db.query(self.model).filter(self.model.user_id == user_id).update(
            {"is_default": False}
        )

        # 设置当前为默认
        db.query(self.model).filter(
            self.model.id == address_id, self.model.user_id == user_id
        ).update({"is_default": True})

        db.commit()

    def delete_user_address(self, db: Session, address_id: int):
        """删除地址"""
        address = self.get(db, address_id)
        if address:
            db.delete(address)
            db.commit()
            return True
        return False


# 创建实例
user_crud = UserCRUD()
address_crud = UserAddressCRUD()
