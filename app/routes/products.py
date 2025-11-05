from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any

from app.dependencies.auth import (
    get_db_dep,
    get_current_user_optional_dep,
    get_pagination_dep,
)
from app.schemas.response import success_response, paginated_response
from app.crud.product import product as product_crud, category as category_crud

router = APIRouter()


@router.get("/products")
async def get_products(
    category_id: Optional[int] = Query(None),
    is_hot: Optional[bool] = Query(None),
    is_new: Optional[bool] = Query(None),
    keyword: Optional[str] = Query(None),
    db: Session = Depends(get_db_dep),
    pagination: dict = Depends(get_pagination_dep),
    current_user: Optional[dict] = Depends(get_current_user_optional_dep),
):
    """获取商品列表"""
    try:
        products = product_crud.get_products_with_filters(
            db,
            category_id=category_id,
            is_hot=is_hot,
            is_new=is_new,
            keyword=keyword,
            skip=pagination["skip"],
            limit=pagination["size"],
        )

        total = product_crud.count_with_filters(
            db, category_id=category_id, is_hot=is_hot, is_new=is_new, keyword=keyword
        )

        # 构建响应数据
        product_list = []
        for product in products:
            product_data = {
                "id": product.id,
                "name": product.name,
                "base_price": float(product.base_price),
                "main_image": product.main_image,
                "is_hot": product.is_hot,
                "is_new": product.is_new,
                "sales_volume": product.sales_volume,
                "month_sales": product.month_sales,
                "stock": product.stock,
                "status": product.status,
            }
            product_list.append(product_data)

        return paginated_response(
            items=product_list,
            total=total,
            page=pagination["page"],
            size=pagination["size"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/categories")
async def get_categories(db: Session = Depends(get_db_dep)):
    """获取分类列表"""
    try:
        categories = category_crud.get_active_categories(db)

        categories_list = []
        for category in categories:
            category_data = {
                "id": category.id,
                "name": category.name,
                "description": category.description,
                "image_url": category.image_url,
                "sort_order": category.sort_order,
                "status": category.status,
            }
            categories_list.append(category_data)

        return success_response(data=categories_list)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/products/{product_id}")
async def get_product_detail(
    product_id: int,
    db: Session = Depends(get_db_dep),
    current_user: Optional[dict] = Depends(get_current_user_optional_dep),
):
    """获取商品详情"""
    try:
        product = product_crud.get_with_specs(db, id=product_id)
        if not product or product.status == 0:
            raise HTTPException(status_code=404, detail="商品不存在")

        # 获取商品规格
        from app.crud.product import product_spec as spec_crud

        specs = spec_crud.get_specs_by_product(db, product_id)

        # 按规格类型分组
        specs_by_type = {}
        for spec in specs:
            spec_type_str = str(spec.spec_type)
            if spec_type_str not in specs_by_type:
                specs_by_type[spec_type_str] = []
            specs_by_type[spec_type_str].append(
                {
                    "id": spec.id,
                    "spec_name": spec.spec_name,
                    "additional_price": float(spec.additional_price),
                    "is_default": spec.is_default,
                    "status": spec.status,
                }
            )

        response_data = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "base_price": float(product.base_price),
            "main_image": product.main_image,
            "image_list": product.image_list or [],
            "is_hot": product.is_hot,
            "is_new": product.is_new,
            "sales_volume": product.sales_volume,
            "month_sales": product.month_sales,
            "stock": product.stock,
            "category_id": product.category_id,
            "category_name": product.category.name if product.category else "",
            "specs": specs_by_type,
        }

        return success_response(data=response_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/products/search")
async def search_products(
    keyword: str = Query(..., min_length=1, max_length=50),
    db: Session = Depends(get_db_dep),
    pagination: dict = Depends(get_pagination_dep),
):
    """搜索商品"""
    try:
        if len(keyword.strip()) < 1:
            raise HTTPException(status_code=400, detail="搜索关键词不能为空")

        products = product_crud.search_products(
            db, keyword=keyword, skip=pagination["skip"], limit=pagination["size"]
        )

        total = product_crud.count_with_filters(db, keyword=keyword)

        product_list = []
        for product in products:
            product_list.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "base_price": float(product.base_price),
                    "main_image": product.main_image,
                    "sales_volume": product.sales_volume,
                }
            )

        return paginated_response(
            items=product_list,
            total=total,
            page=pagination["page"],
            size=pagination["size"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
