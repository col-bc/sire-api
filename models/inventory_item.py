from datetime import datetime

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        Table)

from database import database, metadata

inventory_item = Table(
    'inventory_item',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False),
    Column('image_url', String(255), nullable=False),
    Column('size', String(255), nullable=False),
    Column('sku', String(255), nullable=False),
    Column('upc', String(255), nullable=False),
    Column('shoe_type', String(255), nullable=False),
    Column('brand', String(255), nullable=False),
    Column('market_price', String(255), nullable=False),
    Column('created_at', DateTime, nullable=False, default=datetime.utcnow()),
    Column('updated_at', DateTime, nullable=False, default=datetime.utcnow(), onupdate=datetime.utcnow()),
)

class InventoryItem:
    def __init__(self, name: str, image_url: str, size: str, sku: str, upc: str, shoe_type: str, brand: str, market_price: float):
        self.name = name
        self.image_url = image_url
        self.size = size
        self.sku = sku
        self.upc = upc
        self.shoe_type = shoe_type
        self.brand = brand
        self.market_price = market_price

    def __repr__(self):
        return f"<InventoryItem id:{self.id}"

    def __str__(self):
        return f'InventoryItem {self.id}'

    def __eq__(self, other: 'InventoryItem'):
        return self.id == other.id

    def __ne__(self, other: 'InventoryItem'):
        return not self.__eq__(other)

    def serialize(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'image_url': self.image_url,
            'size': self.size,
            'sku': self.sku,
            'upc': self.upc,
            'shoe_type': self.shoe_type,
            'brand': self.brand,
            'market_price': self.market_price,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
        }
        