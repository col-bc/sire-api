from datetime import datetime

from sqlalchemy import Column, Integer, String, Table

from database import metadata

inventory_shoe = Table(
    'inventory_shoe',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False),
    Column('image', String(255), nullable=True),
    Column('size', String(255), nullable=False),
    Column('sku', String(255), nullable=False),
    Column('upc', String(255), nullable=False),
    Column('shoe_type', String(255), nullable=False),
    Column('brand', String(255), nullable=False),
    Column('market_price', String(255), nullable=False),
)