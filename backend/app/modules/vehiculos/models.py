from sqlalchemy import Column, Integer, String
from ...db.base import Base

class Vehiculo(Base):
    __tablename__ = "vehiculos"
    id = Column(Integer, primary_key=True)
    plate = Column(String)
