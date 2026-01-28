from sqlalchemy import Column, Integer, String
from ...db.base import Base

class CatalogItem(Base):
    __tablename__ = "catalogo"
    id = Column(Integer, primary_key=True)
    name = Column(String)
