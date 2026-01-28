from sqlalchemy import Column, Integer, String
from ...db.base import Base

class Perfil(Base):
    __tablename__ = "perfiles"
    id = Column(Integer, primary_key=True)
    name = Column(String)
