import logging

from ..models import Banner
from .base import CRUDBase

logger = logging.getLogger(__name__)


class BannerCRUD(CRUDBase):
    def __init__(self):
        super().__init__(Banner)


banner_crud = BannerCRUD()
