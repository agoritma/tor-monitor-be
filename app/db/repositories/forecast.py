"""Forecast-related CRUD operations."""

from typing import List
from uuid import UUID

from sqlalchemy import cast, func
from sqlalchemy.dialects.postgresql import DATE as SA_DATE
from sqlmodel import Session, select

from ..models import Sales


def get_sales_dataset_by_goods(
    db: Session, goods_id: UUID, user_id: UUID
) -> List[dict]:
    """Returns sales data for a specific goods grouped by date.

    Prepares the dataset for forecast models by aggregating sales by date
    for a single goods item.

    Args:
        db: Database session
        goods_id: Goods ID to filter sales
        user_id: User ID for ownership validation

    Returns:
        List of dicts with date and total_quantity aggregated by date,
        sorted chronologically
    """
    query = (
        select(
            cast(Sales.sale_date, SA_DATE).label("date"),
            func.sum(Sales.quantity).label("total_quantity"),
        )
        .where(
            Sales.goods_id == goods_id,
            Sales.user_id == user_id,
        )
        .group_by(cast(Sales.sale_date, SA_DATE))
        .order_by(cast(Sales.sale_date, SA_DATE).desc())
        .limit(50)
    )

    results = db.exec(query).all()

    # Convert to list of dicts for dataset
    dataset = []
    for date_val, total_qty in results:
        dataset.append(
            {
                "date": str(date_val),
                "total_quantity": int(total_qty) if total_qty else 0,
            }
        )

    dataset.reverse()
    return dataset
