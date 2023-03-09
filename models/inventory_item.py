from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String,Table

from database import metadata

inventory_shoe = Table(
    'inventory_shoe',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255), nullable=False),
    Column('tags', String(255), default='[]', nullable=False),
    Column('image_url', String(255), nullable=True),
    Column('size', String(255), nullable=False),
    Column('sku', String(255), nullable=False),
    Column('upc', String(255), nullable=False),
    Column('shoe_type', String(255), nullable=False),
    Column('brand', String(255), nullable=False),
    Column('market_price', String(255), nullable=False),
    Column('created_at', DateTime, default=datetime.utcnow()),
    Column('updated_at', DateTime, default=datetime.utcnow(), onupdate=datetime.utcnow()),
)