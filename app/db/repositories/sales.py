"""Sales-related CRUD operations."""

from typing import List, Optional, Tuple
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select

from ..models import Goods, Sales


def get_all_sales(
    db: Session,
    user_id: UUID,
    limit: int = 20,
    page_index: int = 1,
    q: Optional[str] = None,
) -> Tuple[List[Sales], int]:
    """Returns all sales for a user with optional search query on goods name.

    Args:
        db: Database session
        user_id: User ID filter
        limit: Number of items per page
        page_index: Page number (1-indexed)
        q: Search query to filter by goods name

    Returns:
        Tuple of (sales list, total count)

    Raises:
        HTTPException: If no sales found
    """
    query = (
        select(Sales).where(Sales.user_id == user_id).options(selectinload(Sales.goods))
    )

    # Add search filter if query is provided
    if q:
        search_filter = Goods.name.ilike(f"%{q}%")
        query = query.join(Goods).where(search_filter)

    # Get total count before pagination
    count_query = select(Sales).where(Sales.user_id == user_id)
    if q:
        count_query = count_query.join(Goods).where(Goods.name.ilike(f"%{q}%"))

    total_count = len(db.exec(count_query).all())

    # Apply pagination
    if limit:
        query = query.offset((page_index - 1) * limit).limit(limit)

    result = list(db.exec(query).all())
    if not result:
        raise HTTPException(status_code=404, detail="Sales not found")

    return result, total_count


def get_sales_by_id(db: Session, sales_id: UUID, user_id: UUID) -> Sales:
    """Returns a specific sales by its ID for a user.

    Args:
        db: Database session
        sales_id: ID of the sales to retrieve
        user_id: User ID for ownership validation

    Returns:
        Sales object

    Raises:
        HTTPException: If sales not found
    """
    db_sales = db.exec(
        select(Sales).where(Sales.id == sales_id, Sales.user_id == user_id)
    ).first()
    if not db_sales:
        raise HTTPException(status_code=404, detail="Sales not found")

    return db_sales


def create_sales_with_stock_deduction(
    db: Session, sales_data: dict, user_id: UUID
) -> Sales:
    """Creates a sales record and deducts stock from goods.

    Args:
        db: Database session
        sales_data: Dictionary with goods_id, quantity, sale_date
        user_id: User ID for ownership validation

    Returns:
        Created Sales object with total_profit calculated

    Raises:
        HTTPException: If goods not found, insufficient stock, or other errors
    """
    goods_id = sales_data.get("goods_id")
    quantity = sales_data.get("quantity")

    # Get goods to validate stock
    goods = db.exec(
        select(Goods).where(Goods.id == goods_id, Goods.user_id == user_id)
    ).first()

    if not goods:
        raise HTTPException(status_code=404, detail="Goods not found")

    # Validate sufficient stock
    if goods.stock_quantity < quantity:
        raise HTTPException(
            status_code=400,
            detail=f"Insufficient stock. Available: {goods.stock_quantity}, Requested: {quantity}",
        )

    # Calculate total profit (price x quantity)
    total_profit = goods.price * quantity

    # Deduct stock from goods
    goods.stock_quantity -= quantity
    db.add(goods)

    # Create sales record with total_profit
    new_sales = Sales(**sales_data, user_id=user_id, total_profit=total_profit)
    db.add(new_sales)
    db.commit()
    db.refresh(new_sales)

    return new_sales
