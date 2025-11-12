import logging

from sqlalchemy import desc
from sqlalchemy.orm import Session

from ..models import Product
from .base import CRUDBase

logger = logging.getLogger(__name__)


class ProductCRUD(CRUDBase):
    def __init__(self):
        super().__init__(Product)

    def get_hot_products(
        self,
        db: Session,
        field: str,
    ):
        return (
            db.query(self.model)
            .order_by(desc(getattr(self.model, field)))
            .limit(4)
            .all()
        )


product_crud = ProductCRUD()
