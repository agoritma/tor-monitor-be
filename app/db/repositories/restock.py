"""RestockInference-related CRUD operations."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import cast
from sqlalchemy.dialects.postgresql import DATE as SA_DATE
from sqlmodel import Session, select

from ..models import RestockInference
from .goods import get_goods_by_id


def get_restock_inference_by_goods(
    db: Session, goods_id: UUID, user_id: UUID
) -> Optional[RestockInference]:
    """Get the latest RestockInference for a specific goods by user.

    Args:
        db: Database session
        goods_id: ID of the goods
        user_id: User ID for ownership validation

    Returns:
        RestockInference object or None if not found
    """
    # Validate goods ownership
    get_goods_by_id(db, goods_id, user_id)

    query = select(RestockInference).where(RestockInference.goods_id == goods_id)
    return db.exec(query).first()


def get_restock_inference_by_goods_and_date(
    db: Session, goods_id: UUID, user_id: UUID
) -> Optional[RestockInference]:
    """Get RestockInference created today for a specific goods.

    Args:
        db: Database session
        goods_id: ID of the goods
        user_id: User ID for ownership validation

    Returns:
        RestockInference object created today or None if not found
    """
    # Validate goods ownership
    get_goods_by_id(db, goods_id, user_id)

    today = datetime.now().date()
    query = (
        select(RestockInference)
        .where(RestockInference.goods_id == goods_id)
        .where(cast(RestockInference.created_at, SA_DATE) == today)
    )
    return db.exec(query).first()


def create_restock_inference(
    db: Session,
    goods_id: UUID,
    total_quantity: int,
    future_preds: Optional[dict] = None,
) -> RestockInference:
    """Create a new RestockInference record.

    Args:
        db: Database session
        goods_id: ID of the goods
        total_quantity: Total predicted quantity
        future_preds: Optional dict with future predictions

    Returns:
        Created RestockInference object
    """
    inference = RestockInference(
        goods_id=goods_id,
        total_quantity=total_quantity,
        future_preds=future_preds,
    )
    db.add(inference)
    db.commit()
    db.refresh(inference)
    return inference


def update_restock_inference(
    db: Session,
    inference_id: UUID,
    total_quantity: Optional[int] = None,
    future_preds: Optional[dict] = None,
) -> RestockInference:
    """Update an existing RestockInference record.

    Args:
        db: Database session
        inference_id: ID of the inference record to update
        total_quantity: New total quantity (optional)
        future_preds: New future predictions (optional)

    Returns:
        Updated RestockInference object

    Raises:
        HTTPException: If RestockInference not found
    """
    inference = db.exec(
        select(RestockInference).where(RestockInference.id == inference_id)
    ).first()
    if not inference:
        raise HTTPException(status_code=404, detail="RestockInference not found")

    if total_quantity is not None:
        inference.total_quantity = total_quantity
    if future_preds is not None:
        inference.future_preds = future_preds

    db.add(inference)
    db.commit()
    db.refresh(inference)
    return inference
