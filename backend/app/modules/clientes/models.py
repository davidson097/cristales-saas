import uuid
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from ...db.base import Base

class Cliente(Base):
    __tablename__ = "clientes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
