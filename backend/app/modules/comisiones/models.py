from sqlalchemy import Column, Integer, String
from ...db.base import Base

class Comision(Base):
    __tablename__ = "comisiones"
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
