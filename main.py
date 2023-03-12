from datetime import datetime
from typing import List
from uuid import uuid4

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyQuery
from jose import JWTError, jwt

import utilities
from database import database, engine, metadata
from models.inventory_item import inventory_shoe
from schemas.inventory_schema import ItemSchema, ItemSchemaIn

metadata.create_all(engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['localhost:8080', 'sireapp.io'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


token_scheme = APIKeyQuery(name="access_token", auto_error=False)

def verify_token(token: str):
    if token is None:
        raise HTTPException(status_code=401, detail="access_token is required")

    try:
        payload = jwt.decode(token, 'inventory-secret-key', algorithms=['HS256'])
    except JWTError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid token")
    


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/inventory", status_code=200)
async def read_inventory(limit: int = 10, page: int = 0, token: str = Depends(token_scheme)):
    verify_token(token)
   
    query = inventory_shoe.select().limit(limit).offset(page * limit)
    items = await database.fetch_all(query)
    return {
        'items': items,
        'page': page,
        'pages': len(items) // limit 
    }


@app.post("/inventory", response_model=ItemSchema, status_code=201)
async def create_inventory_shoe(item: ItemSchemaIn, token: str = Depends(token_scheme)):
    verify_token(token)
    
    print(item)
    
    query = inventory_shoe.insert().values(
        name=item.name,
        image=item.image,
        size=item.size,
        sku=item.sku,
        upc=item.upc,
        shoe_type=item.shoe_type,
        brand=item.brand,
        market_price=item.market_price,
    )
    inserted_id = await database.execute(query)
    return {**item.dict(), "id": inserted_id}


@app.get("/inventory/{item_id}", response_model=ItemSchema, status_code=200)
async def read_item(item_id: int, token: str = Depends(token_scheme)):
    verify_token(token)
    
    query = inventory_shoe.select().where(
        inventory_shoe.c.id == item_id
    )
    item = await database.fetch_one(query)
    return item


@app.put("/inventory/{item_id}", response_model=ItemSchema, status_code=201)
async def update_item(item_id: int, item: ItemSchemaIn, token: str = Depends(token_scheme)):
    verify_token(token)
    
    query = (
        inventory_shoe.update()
        .where(inventory_shoe.c.id == item_id)
        .values(
            name=item.name,
            image=item.image if item.image else None,
            size=item.size,
            sku=item.sku,
            upc=item.upc,
            shoe_type=item.shoe_type,
            brand=item.brand,
            market_price=item.market_price,
        )
        .returning(inventory_shoe.c.id)
    )
    updated_id = await database.execute(query)
    return {**item.dict(), "id": updated_id}


@app.get('/inventory/search/{query}', response_model=List[ItemSchema], status_code=200)
async def search_inventory(query: str, token: str = Depends(token_scheme)):
    verify_token(token)
    
    items = []
    
    # Search by name
    q1 = inventory_shoe.select().where(
        inventory_shoe.c.name.ilike(f'%{query}%'))
    items.extend(await database.fetch_all(q1))
    
    # Search by sku
    q2 = inventory_shoe.select().where(
        inventory_shoe.c.sku.ilike(f'%{query}%'))
    items.extend(await database.fetch_all(q2))
    
    if (len(items) == 0):
        raise HTTPException(status_code=404, detail="No items found")
    return items
