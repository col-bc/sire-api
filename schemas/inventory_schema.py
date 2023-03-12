from typing import Union

from pydantic import BaseModel


class ItemSchemaIn(BaseModel):
    name: str
    image: Union[str, None] = None
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

    class Config:
        orm_mode = True
