import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from ...db.base import Base


class Empresa(Base):
    __tablename__ = "empresas"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(255), nullable=False, unique=True)
    razon_social = Column(String(255), nullable=True)
    rfc = Column(String(13), nullable=True, unique=True)
    email = Column(String(255), nullable=True)
    telefono = Column(String(20), nullable=True)
    direccion = Column(Text, nullable=True)
    ciudad = Column(String(100), nullable=True)
    pais = Column(String(100), nullable=True, default="Mexico")
    estado = Column(Boolean, default=True, nullable=False)
    descripcion = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Empresa {self.nombre}>"
