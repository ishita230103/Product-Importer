from sqlalchemy import Column, Integer, String, Boolean, Text
from backend.app.db.base import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, nullable=False)
    sku_lower = Column(String, unique=True, nullable=False)
    name = Column(String)
    description = Column(Text)
    active = Column(Boolean, default=True)


class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    event = Column(String)
    enabled = Column(Boolean, default=True)
