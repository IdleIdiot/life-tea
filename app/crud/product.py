from sqlalchemy.orm import Session

from app.models.product import Category
from app.dependencies import get_db


class CategoryCRUD:
    """用户 CRUD 操作"""

    def __init__(self):
        self.model = Category

    def get(self, db: Session, category_id: int):
        """根据ID获取用户"""
        return db.query(self.model).filter(self.model.id == category_id).first()


category_crud = CategoryCRUD()


if __name__ == "__main__":
    print(CategoryCRUD().get(next(get_db()), 1).image_url)
