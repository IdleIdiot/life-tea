from typing import Optional

from models.shop import Shop
from schemas.shop import ShopCreate, ShopUpdate
from sqlalchemy.orm import Session

from .base import CRUDBase


class ShopCRUD(CRUDBase):
    def __init__(self):
        super().__init__(Shop)

    def get_active_shop(self, db: Session) -> Optional[Shop]:
        """获取当前营业的店铺（通常只有一个）"""
        return db.query(self.model).filter(self.model.is_active).first()

    def update_shop(
        self, db: Session, shop_id: int, shop_update: ShopUpdate
    ) -> Optional[Shop]:
        """更新店铺信息"""
        db_shop = self.get(db, shop_id)
        if not db_shop:
            return None

        update_data = shop_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_shop, field, value)

        self.db.commit()
        self.db.refresh(db_shop)
        return db_shop

    def toggle_shop_status(self, shop_id: int) -> Optional[Shop]:
        """切换店铺营业状态"""
        db_shop = self.get(shop_id)
        if not db_shop:
            return None

        db_shop.is_active = not db_shop.is_active
        self.db.commit()
        self.db.refresh(db_shop)
        return db_shop


# 创建全局实例

shop_crud = ShopCRUD()
