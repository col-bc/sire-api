from datetime import datetime
from typing import List
from uuid import uuid4

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.security.api_key import APIKeyHeader
from jose import JWTError, jwt

from models.inventory_item import inventory_shoe
import utilities
from database import database, engine, metadata
from schemas.inventory_schema import ItemSchema, ItemSchemaIn

metadata.create_all(engine)

app = FastAPI()

oauth2_scheme = APIKeyHeader(name="access_token", auto_error=False)

def verify_token(token: str):
    if token is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    try:
        payload = jwt.decode(token, 'inventory-secret-key', algorithms=['HS256'])
        print(payload)
    except JWTError as e:
        print(e)
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return True


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/inventory", response_model=List[ItemSchema], status_code=200)
async def read_inventory(token: str = Depends(oauth2_scheme)):
    verify_token(token)
   
    query = inventory_shoe.select()
    items = await database.fetch_all(query)
    return items 


@app.post("/inventory", response_model=ItemSchema, status_code=201)
async def create_inventory_shoe(item: ItemSchemaIn, token: str = Depends(oauth2_scheme)):
    verify_token(token)
    
    print(item)
    
    query = inventory_shoe.insert().values(
        name=item.name,
        tags=item.tags if item.tags else '[]',
        image_url=item.image_url if item.image_url else None,
        size=item.size,
        sku=item.sku,
        upc=item.upc,
        shoe_type=item.shoe_type,
        brand=item.brand,
        market_price=item.market_price,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    inserted_id = await database.execute(query)
    return {**item.dict(), "id": inserted_id}


@app.get("/inventory/{item_id}", response_model=ItemSchema, status_code=200)
async def read_item(item_id: int, token: str = Depends(oauth2_scheme)):
    verify_token(token)
    
    query = inventory_shoe.select().where(
        inventory_shoe.c.id == item_id
    )
    item = await database.fetch_one(query)
    return item


@app.put("/inventory/{item_id}", response_model=ItemSchema, status_code=201)
async def update_item(item_id: int, item: ItemSchemaIn, token: str = Depends(oauth2_scheme)):
    verify_token(token)
    
    query = (
        inventory_shoe.update()
        .where(inventory_shoe.c.id == item_id)
        .values(
            name=item.name,
            tags=item.tags if item.tags else '[]',
            image_url=item.image_url if item.image_url else None,
            size=item.size,
            sku=item.sku,
            upc=item.upc,
            shoe_type=item.shoe_type,
            brand=item.brand,
            market_price=item.market_price,
            updated_at=datetime.utcnow()
        )
        .returning(inventory_shoe.c.id)
    )
    updated_id = await database.execute(query)
    return {**item.dict(), "id": updated_id}


@app.post("/inventory/{item_id}/image",  status_code=201)
async def upload_image(item_id: int, image: UploadFile = File(...), token: str = Depends(oauth2_scheme)):
    verify_token(token)
    
    item = read_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    if item.image_url:
        # Delete the old image from cloud storage
        if not utilities.delete_blob('sire_inventory', item.image_url.split('/')[-1]):
            raise HTTPException(status_code=500, detail="Could not delete existing image")
    
    # Upload the image to cloud storage
    contents = image.file.read()
    uid = uuid4().hex
    if not utilities.upload_blob('sire_inventory', contents, uid):
        raise HTTPException(status_code=500, detail="Could not upload image")

    # Update the db item with the new image url
    query = (
        inventory_shoe.update()
        .where(inventory_shoe.c.id == item_id)
        .values(
            image_url=f'https://storage.googleapis.com/sire_inventory/{uid}',
            updated_at=datetime.utcnow()
        )
    )
    await database.execute(query)
    return {"image_url": f'https://storage.googleapis.com/sire_inventory/{uid}'}
    

        