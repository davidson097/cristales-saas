from sqlalchemy import Column, Integer, String
from ...db.base import Base

class StockItem(Base):
    __tablename__ = "stock"
    id = Column(Integer, primary_key=True)
    name = Column(String)
