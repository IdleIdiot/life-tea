import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..crud import banner_crud
from ..dependencies import get_db
from ..schemas import BannerListResponse, ResponseModel, success_response

logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/banners", response_model=ResponseModel[BannerListResponse])
async def get_banners(db: Session = Depends(get_db)):
    banners = banner_crud.get_all(db=db)
    result = BannerListResponse(items=banners)

    return success_response(data=result)
