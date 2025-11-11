from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..dependencies import get_db
from ..schemas import success_response, ResponseModel, ProductListResponse
from ..crud import product_crud

import logging

logger = logging.getLogger(__name__)


router = APIRouter()


@router.get("/products", response_model=ResponseModel[ProductListResponse])
async def get_products(db: Session = Depends(get_db)):
    products = product_crud.get_all(db=db)
    result = ProductListResponse(items=products)
    return success_response(data=result)
