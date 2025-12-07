"""Generic CRUD operations for all database models."""

from pydantic import BaseModel
from sqlmodel import Session, SQLModel


def update_db_element(
    db: Session, original_element: SQLModel, element_update: BaseModel
) -> BaseModel:
    """Updates an element in database.

    Args:
        db: Database session
        original_element: The existing model instance to update
        element_update: Pydantic model with updated values

    Returns:
        Updated model instance
    """
    update_data = element_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(original_element, key, value)

    db.add(original_element)
    db.commit()
    db.refresh(original_element)

    return original_element


def delete_db_element(db: Session, element: SQLModel) -> None:
    """Deletes an element from database.

    Args:
        db: Database session
        element: The model instance to delete
    """
    db.delete(element)
    db.commit()
