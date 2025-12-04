from uuid import UUID
from sqlmodel import SQLModel
from datetime import datetime
from typing import Optional


class GoodsBase(SQLModel):
    id: UUID
    name: str
    category: Optional[str] = None


class SalesBase(SQLModel):
    id: UUID
    goods_id: UUID
    quantity: int
    sale_date: datetime
    total_profit: Optional[float] = None
    goods: GoodsBase


class SalesAllResponse(SQLModel):
    data: list[SalesBase]
    total: int
    page: int
    limit: int


class SalesCreate(SQLModel):
    goods_id: UUID
    quantity: int
    sale_date: datetime


class SalesUpdate(SQLModel):
    quantity: int
    sale_date: datetime
