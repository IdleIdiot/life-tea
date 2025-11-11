import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..crud import category_crud
from ..dependencies import get_db
from ..schemas import CategoryListResponse, ResponseModel, success_response

logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/categories", response_model=ResponseModel[CategoryListResponse])
async def get_categories(db: Session = Depends(get_db)):
    categories = category_crud.get_all(db=db)
    result = CategoryListResponse(items=categories)
    return success_response(data=result)
