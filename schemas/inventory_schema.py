from pydantic import BaseModel
from datetime import datetime

class ItemSchemaIn(BaseModel):
    name: str
    tags: str | None = None
    image_url: str | None = None
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
    created_at: datetime | None = datetime.utcnow()
    updated_at: datetime | None = datetime.utcnow()

    class Config:
        orm_mode = True
    
