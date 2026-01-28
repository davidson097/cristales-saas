from sqlalchemy import Column, Integer, String
from ...db.base import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    username = Column(String)
