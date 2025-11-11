from ..models import Product
from .base import CRUDBase

import logging

logger = logging.getLogger(__name__)


class ProductCRUD(CRUDBase):
    def __init__(self):
        super().__init__(Product)


product_crud = ProductCRUD()
