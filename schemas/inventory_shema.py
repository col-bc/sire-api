from pydantic import BaseModel
from datetime import datetime

class ItemSchemaIn(BaseModel):
    name: str
    image_url: str
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
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
    