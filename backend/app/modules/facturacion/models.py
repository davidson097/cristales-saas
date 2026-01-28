from sqlalchemy import Column, Integer, String
from ...db.base import Base

class Factura(Base):
    __tablename__ = "facturas"
    id = Column(Integer, primary_key=True)
    total = Column(Integer)
