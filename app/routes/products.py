import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..crud import product_crud
from ..dependencies import get_db
from ..schemas import ProductListResponse, ResponseModel, success_response

logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/products", response_model=ResponseModel[ProductListResponse])
async def get_products(db: Session = Depends(get_db)):
    products = product_crud.get_all(db=db)
    result = ProductListResponse(items=products)
    return success_response(data=result)
