from sqlalchemy import Column, Integer, String
from ...db.base import Base

class Zona(Base):
    __tablename__ = "zonas"
    id = Column(Integer, primary_key=True)
    name = Column(String)
