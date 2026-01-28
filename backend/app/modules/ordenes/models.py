from sqlalchemy import Column, Integer, String
from ...db.base import Base

class Orden(Base):
    __tablename__ = "ordenes"
    id = Column(Integer, primary_key=True)
    description = Column(String)
