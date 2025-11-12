import logging
from typing import List, Optional

from sqlalchemy.orm import Session, joinedload

from ..models import Category
from .base import CRUDBase

logger = logging.getLogger(__name__)


class CategoryCRUD(CRUDBase):
    def __init__(self):
        super().__init__(Category)

    def get_all_with_products(self, db: Session) -> List[Category]:
        """获取所有分类及其关联的产品"""
        return (
            db.query(self.model)
            .options(joinedload(self.model.products))  # 使用joinedload预加载产品
            .order_by(self.model.sort_order.desc(), self.model.id.asc())
            .all()
        )

    def get_with_products(self, db: Session, category_id: int) -> Optional[Category]:
        """根据ID获取分类及其关联的产品"""
        return (
            db.query(self.model)
            .options(joinedload(self.model.products))
            .filter(self.model.id == category_id)
            .first()
        )


category_crud = CategoryCRUD()
