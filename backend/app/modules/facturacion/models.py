import uuid
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from ...db.base import Base

class Factura(Base):
    __tablename__ = "facturas"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    total = Column(Integer)
