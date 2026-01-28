from sqlalchemy import Column, Integer, String
from ...db.base import Base

class Pago(Base):
    __tablename__ = "pagos"
    id = Column(Integer, primary_key=True)
    amount = Column(Integer)
