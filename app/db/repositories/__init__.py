"""Repository layer for database operations.

This package provides domain-specific repository modules for CRUD operations,
organized by business domain for better maintainability and scalability.

Modules:
    generic: Generic CRUD operations (update, delete)
    goods: Goods inventory operations
    sales: Sales transaction operations
    dashboard: Dashboard analytics queries
    forecast: Sales forecast dataset operations
    restock: Restock inference prediction operations
"""

from .dashboard import (
    get_monthly_revenue,
    get_sales_chart_data,
    get_top_selling_item,
)
from .forecast import get_sales_dataset_by_goods
from .generic import delete_db_element, update_db_element
from .goods import (
    get_all_goods,
    get_goods_by_id,
    get_goods_with_relations,
    get_top_low_stock_goods,
)
from .restock import (
    create_restock_inference,
    get_restock_inference_by_goods,
    get_restock_inference_by_goods_and_date,
    update_restock_inference,
)
from .sales import (
    create_sales_with_stock_deduction,
    get_all_sales,
    get_sales_by_id,
)

__all__ = [
    # Generic operations
    "update_db_element",
    "delete_db_element",
    # Goods operations
    "get_all_goods",
    "get_goods_by_id",
    "get_goods_with_relations",
    "get_top_low_stock_goods",
    # Sales operations
    "get_all_sales",
    "get_sales_by_id",
    "create_sales_with_stock_deduction",
    # Dashboard operations
    "get_sales_chart_data",
    "get_monthly_revenue",
    "get_top_selling_item",
    # Forecast operations
    "get_sales_dataset_by_goods",
    # Restock operations
    "get_restock_inference_by_goods",
    "get_restock_inference_by_goods_and_date",
    "create_restock_inference",
    "update_restock_inference",
]
