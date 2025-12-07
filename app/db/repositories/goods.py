"""Goods-related CRUD operations."""

from typing import List, Optional, Tuple
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import or_
from sqlmodel import Session, select

from ..models import Goods


def get_all_goods(
    db: Session, user_id: UUID, limit: int, page_index: int, q: Optional[str] = None
) -> Tuple[List[Goods], int]:
    """Returns all goods for a user with optional search query.

    Args:
        db: Database session
        user_id: User ID filter
        limit: Number of items per page
        page_index: Page number (1-indexed)
        q: Search query to filter by name or category

    Returns:
        Tuple of (goods list, total count)
    """
    query = select(Goods).where(Goods.user_id == user_id)

    if q:
        search_filter = or_(Goods.name.ilike(f"%{q}%"), Goods.category.ilike(f"%{q}%"))
        query = query.where(search_filter)

    count_query = select(Goods).where(Goods.user_id == user_id)
    if q:
        search_filter = or_(Goods.name.ilike(f"%{q}%"), Goods.category.ilike(f"%{q}%"))
        count_query = count_query.where(search_filter)

    total_count = len(db.exec(count_query).all())

    if limit:
        query = query.offset((page_index - 1) * limit).limit(limit)

    db_goods = list(db.exec(query).all())
    if not db_goods:
        raise HTTPException(status_code=404, detail="Goods not found")

    return db_goods, total_count


def get_goods_by_id(db: Session, goods_id: UUID, user_id: UUID) -> Goods:
    """Returns a specific goods by its ID for a user.

    Args:
        db: Database session
        goods_id: ID of the goods to retrieve
        user_id: User ID for ownership validation

    Returns:
        Goods object

    Raises:
        HTTPException: If goods not found
    """
    db_goods = db.exec(
        select(Goods).where(Goods.id == goods_id, Goods.user_id == user_id)
    ).first()
    if not db_goods:
        raise HTTPException(status_code=404, detail="Goods not found")

    return db_goods


def get_goods_with_relations(db: Session, goods_id: UUID, user_id: UUID) -> Goods:
    """Returns a specific goods by its ID for a user, including relations.

    Args:
        db: Database session
        goods_id: ID of the goods to retrieve
        user_id: User ID for ownership validation

    Returns:
        Goods object with loaded relations

    Raises:
        HTTPException: If goods not found
    """
    q = select(Goods).where(Goods.id == goods_id, Goods.user_id == user_id)
    result = db.exec(q).one_or_none()
    if result is None:
        raise HTTPException(status_code=404, detail="Goods not found")
    return result


def get_top_low_stock_goods(db: Session, user_id: UUID, limit: int = 10) -> List[Goods]:
    """Returns top N goods with lowest stock quantity.

    Args:
        db: Database session
        user_id: User ID filter
        limit: Number of items to return (default 10)

    Returns:
        List of Goods ordered by stock_quantity ascending
    """
    query = (
        select(Goods)
        .where(Goods.user_id == user_id)
        .order_by(Goods.stock_quantity.asc())
        .limit(limit)
    )
    goods = db.exec(query).all()
    return list(goods) if goods else []
