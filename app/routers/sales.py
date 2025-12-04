import logging
from uuid import UUID

from fastapi import APIRouter, HTTPException
from ..db import crud
from ..dependencies import DBSessionDependency, UserDependency
from ..schemas.sales import SalesCreate, SalesUpdate, SalesAllResponse
from typing import Optional

logger = logging.getLogger(__name__)
router = APIRouter(tags=["sales"])


@router.get("/api/sales")
def get_sales(
    db: DBSessionDependency,
    user: UserDependency,
    limit: int = 20,
    page_index: int = 1,
    q: Optional[str] = None,
) -> SalesAllResponse:
    try:
        sales, total = crud.get_all_sales(
            db, user_id=user.id, limit=limit, page_index=page_index, q=q
        )
        return {"data": sales, "total": total, "page": page_index, "limit": limit}
    except Exception as e:
        logging.error("Error fetching sales %s", e)
        raise HTTPException(status_code=400, detail="Error fetching sales")


@router.post("/api/sales")
def create_sales(db: DBSessionDependency, sales: SalesCreate, user: UserDependency):
    try:
        new_sales = crud.create_sales_with_stock_deduction(
            db, sales.model_dump(), user_id=user.id
        )
        return {"message": "Sales created successfully", "data": new_sales}
    except HTTPException:
        raise
    except Exception as e:
        logging.error("Error during sales creation %s", e)
        raise HTTPException(status_code=400, detail="Error during sales creation")


@router.put("/api/sales/{sales_id}")
def update_sales(
    sales_id: UUID,
    sales_update: SalesUpdate,
    db: DBSessionDependency,
    user: UserDependency,
):
    db_sales = crud.get_sales_by_id(db, sales_id=sales_id, user_id=user.id)
    if db_sales is None:
        logging.error("Goods not found for id %s", sales_id)
        raise HTTPException(status_code=404, detail="Goods not found")
    updated_sales = crud.update_db_element(
        db=db, original_element=db_sales, element_update=sales_update
    )
    return updated_sales


@router.delete("/api/sales/{sales_id}")
def delete_sales(sales_id: UUID, db: DBSessionDependency, user: UserDependency):
    db_sales = crud.get_sales_by_id(db, user_id=user.id, sales_id=sales_id)
    if db_sales is None:
        logging.error("Goods not found for id %s", sales_id)
        raise HTTPException(status_code=404, detail="Goods not found")

    db.delete(db_sales)
    db.commit()
    return {"message": "Sales deleted successfully", "data": db_sales}
