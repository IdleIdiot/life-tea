import logging

from ..models import Category
from .base import CRUDBase

logger = logging.getLogger(__name__)


class CategoryCRUD(CRUDBase):
    def __init__(self):
        super().__init__(Category)


category_crud = CategoryCRUD()
