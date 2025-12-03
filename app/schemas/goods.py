from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class GoodsResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    category: Optional[str] = None
    price: float
    stock_quantity: int
