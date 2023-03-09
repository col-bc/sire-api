from pydantic import BaseModel
from datetime import datetime

class ItemSchemaIn(BaseModel):
    name: str
    tags: str | None
    image_url: str | None
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
    created_at: datetime | None
    updated_at: datetime | None

    class Config:
        orm_mode = True
    