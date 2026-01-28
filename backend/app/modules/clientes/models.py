from sqlalchemy import Column, Integer, String
from ...db.base import Base

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(Integer, primary_key=True)
    name = Column(String)
