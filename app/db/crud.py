from typing import List
from uuid import UUID

from fastapi import HTTPException
from pydantic import BaseModel
from sqlmodel import Session, SQLModel, select

from .models import Goods, RestockInference, Sales

######################################################
# Generic CRUD operations
######################################################


def update_db_element(
    db: Session, original_element: SQLModel, element_update: BaseModel
) -> BaseModel:
    """Updates an element in database.
    Note that it doesn't take care of user ownership.
    """
    update_data = element_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(original_element, key, value)

    db.add(original_element)
    db.commit()
    db.refresh(original_element)

    return original_element


def delete_db_element(db: Session, element: SQLModel):
    """Deletes an element from database."""
    db.delete(element)
    db.commit()


######################################################
# Specific CRUD operations
######################################################


def get_goods(db: Session, goods_id: UUID, user_id: UUID) -> Goods:
    """Returns a specific goods by its ID for a user. if goods_id is None, return all goods"""
    if goods_id is None:
        return db.exec(select(Goods).where(Goods.user_id == user_id)).all()

    db_goods = db.exec(
        select(Goods).where(Goods.id == goods_id, Goods.user_id == user_id)
    ).first()
    if not db_goods:
        raise HTTPException(status_code=404, detail="Goods not found")

    return db_goods


def get_sales(db: Session, user_id: UUID) -> List[Sales]:
    """Returns all sales for a user."""
    sales = db.exec(select(Sales).where(Sales.user_id == user_id)).all()
    return sales
