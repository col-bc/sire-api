from datetime import datetime
from typing import Union

from pydantic import BaseModel


class ItemSchemaIn(BaseModel):
    name: str
    tags: Union[str, None] = None
    image_url: Union[str, None] = None
    size: str
    sku: str
    upc: str
    shoe_type: str
    brand: str
    market_price: float

    class Config:
        orm_mode = True
        
class ItemSchema(ItemSchemaIn):
    id: int
    created_at: Union[datetime, None] = datetime.utcnow()
    updated_at: Union[datetime, None] = datetime.utcnow()

    class Config:
        orm_mode = True
