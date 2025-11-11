from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..dependencies import get_db
from ..schemas import success_response, ResponseModel, BannerListResponse
from ..crud import banner_crud

import logging

logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/banners", response_model=ResponseModel[BannerListResponse])
async def get_banners(db: Session = Depends(get_db)):
    banners = banner_crud.get_all(db=db)
    result = BannerListResponse(items=banners)

    return success_response(data=result)
