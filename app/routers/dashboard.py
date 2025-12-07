import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException

from ..db import crud
from ..dependencies import DBSessionDependency, UserDependency
from ..schemas.dashboard import DashboardResponse, TopSellingItem

logger = logging.getLogger(__name__)
router = APIRouter(tags=["dashboard"])


@router.get("/api/dashboard/")
def get_dashboard(
    db: DBSessionDependency,
    user: UserDependency,
    year: Optional[int] = None,
    month: Optional[int] = None,
) -> DashboardResponse:
    """Get dashboard data with optional year and month filter.

    If year and month are not provided, uses current year and month.
    """
    try:
        # Default to current year and month if not provided
        if year is None or month is None:
            now = datetime.now()
            year = year or now.year
            month = month or now.month

        # Validate year and month
        if not (1 <= month <= 12):
            raise HTTPException(
                status_code=400, detail="Month must be between 1 and 12"
            )
        if year < 2000 or year > 2099:
            raise HTTPException(
                status_code=400, detail="Year must be between 2000 and 2099"
            )

        # Get all dashboard data
        top_low_stock = crud.get_top_low_stock_goods(db, user_id=user.id, limit=10)
        sales_chart = crud.get_sales_chart_data(
            db, user_id=user.id, year=year, month=month
        )
        monthly_revenue = crud.get_monthly_revenue(
            db, user_id=user.id, year=year, month=month
        )
        top_selling_item_data = crud.get_top_selling_item(
            db, user_id=user.id, year=year, month=month
        )

        # Handle case when there's no top selling item
        if top_selling_item_data is None:
            top_selling_item = TopSellingItem(
                name="N/A", total_quantity_sold=0, total_profit=0.0
            )
        else:
            top_selling_item = TopSellingItem(**top_selling_item_data)

        # Build response
        return {
            "data": {
                "top_low_stock": top_low_stock,
                "sales_chart": sales_chart,
                "monthly_revenue": monthly_revenue,
                "top_selling_item": top_selling_item,
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        logging.error("Error fetching dashboard data %s", e)
        raise HTTPException(status_code=400, detail="Error fetching dashboard data")
