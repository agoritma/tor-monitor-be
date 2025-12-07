"""Dashboard analytics CRUD operations."""

from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import cast, func
from sqlalchemy.dialects.postgresql import DATE as SA_DATE
from sqlmodel import Session, select

from ..models import Goods, Sales


def get_sales_chart_data(
    db: Session, user_id: UUID, year: int, month: int
) -> List[dict]:
    """Returns sales data aggregated by date for chart visualization.

    Args:
        db: Database session
        user_id: User ID filter
        year: Year to filter
        month: Month to filter

    Returns:
        List of dicts with date, total_quantity, and total_sales
    """
    query = (
        select(
            cast(Sales.sale_date, SA_DATE).label("date"),
            func.sum(Sales.quantity).label("total_quantity"),
            func.sum(Sales.total_profit).label("total_sales"),
        )
        .where(
            Sales.user_id == user_id,
            func.extract("year", Sales.sale_date) == year,
            func.extract("month", Sales.sale_date) == month,
        )
        .group_by(cast(Sales.sale_date, SA_DATE))
        .order_by(cast(Sales.sale_date, SA_DATE))
    )

    results = db.exec(query).all()

    # Convert to list of dicts
    chart_data = []
    for date_val, total_quantity, total in results:
        chart_data.append(
            {
                "date": str(date_val),
                "total_quantity": int(total_quantity) if total_quantity else 0,
                "total_sales": float(total) if total else 0.0,
            }
        )

    return chart_data


def get_monthly_revenue(db: Session, user_id: UUID, year: int, month: int) -> float:
    """Returns total revenue for a specific month.

    Args:
        db: Database session
        user_id: User ID filter
        year: Year to filter
        month: Month to filter

    Returns:
        Total revenue (sum of total_profit)
    """
    query = select(func.sum(Sales.total_profit)).where(
        Sales.user_id == user_id,
        func.extract("year", Sales.sale_date) == year,
        func.extract("month", Sales.sale_date) == month,
    )

    result = db.exec(query).first()
    return float(result) if result else 0.0


def get_top_selling_item(
    db: Session, user_id: UUID, year: int, month: int
) -> Optional[dict]:
    """Returns the top selling item (by quantity) for a specific month.

    Args:
        db: Database session
        user_id: User ID filter
        year: Year to filter
        month: Month to filter

    Returns:
        Dict with name, total_quantity_sold, and total_profit, or None if no sales
    """
    query = (
        select(
            Goods.name,
            func.sum(Sales.quantity).label("total_quantity"),
            func.sum(Sales.total_profit).label("total_profit"),
        )
        .join(Sales, Sales.goods_id == Goods.id)
        .where(
            Sales.user_id == user_id,
            func.extract("year", Sales.sale_date) == year,
            func.extract("month", Sales.sale_date) == month,
        )
        .group_by(Goods.name)
        .order_by(func.sum(Sales.quantity).desc())
        .limit(1)
    )

    result = db.exec(query).first()

    if result:
        return {
            "name": result[0],
            "total_quantity_sold": int(result[1]),
            "total_profit": float(result[2]) if result[2] else 0.0,
        }

    return None
