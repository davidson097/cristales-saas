import uuid
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from ...db.base import Base


class TipoMovimientoInventario(Enum):
    ENTRADA = "ENTRADA"
    SALIDA = "SALIDA"
    AJUSTE = "AJUSTE"
    DEVOLUCION = "DEVOLUCION"


class SeveridadAlerta(Enum):
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class EstadoAlerta(Enum):
    ABIERTA = "ABIERTA"
    VISTA = "VISTA"
    RESUELTA = "RESUELTA"


class Almacen(Base):
    __tablename__ = "almacenes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empresa_id = Column(UUID(as_uuid=True), ForeignKey("empresas.id"), nullable=False)
    nombre = Column(String(255), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    # Relationships
    empresa = relationship("Empresa", back_populates="almacenes")


class StockConfig(Base):
    __tablename__ = "stock_config"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empresa_id = Column(UUID(as_uuid=True), ForeignKey("empresas.id"), nullable=False)
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("almacenes.id"), nullable=False)
    cristal_id = Column(UUID(as_uuid=True), ForeignKey("catalogo.id"), nullable=False)
    stock_min = Column(Integer, default=0, nullable=False)
    stock_max = Column(Integer, default=1000, nullable=False)

    # Relationships
    empresa = relationship("Empresa")
    almacen = relationship("Almacen")
    cristal = relationship("CatalogItem")


class MovimientoInventario(Base):
    __tablename__ = "movimientos_inventario"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empresa_id = Column(UUID(as_uuid=True), ForeignKey("empresas.id"), nullable=False)
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("almacenes.id"), nullable=False)
    cristal_id = Column(UUID(as_uuid=True), ForeignKey("catalogo.id"), nullable=False)
    tipo = Column(String(20), nullable=False)  # Using string for enum
    cantidad = Column(Integer, nullable=False)
    costo_unit = Column(Numeric(12, 2), nullable=True)
    ref_tipo = Column(String(50), nullable=True)
    ref_id = Column(UUID(as_uuid=True), nullable=True)
    nota = Column(Text, nullable=True)
    creado_en = Column(DateTime, default=datetime.utcnow, nullable=False)
    creado_por = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=True)

    # Relationships
    empresa = relationship("Empresa")
    almacen = relationship("Almacen")
    cristal = relationship("CatalogItem")
    usuario = relationship("Usuario")


class AlertaStock(Base):
    __tablename__ = "alertas_stock"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    empresa_id = Column(UUID(as_uuid=True), ForeignKey("empresas.id"), nullable=False)
    almacen_id = Column(UUID(as_uuid=True), ForeignKey("almacenes.id"), nullable=False)
    cristal_id = Column(UUID(as_uuid=True), ForeignKey("catalogo.id"), nullable=False)
    stock_min = Column(Integer, default=0, nullable=False)
    stock_actual = Column(Integer, default=0, nullable=False)
    severidad = Column(String(20), default="WARNING", nullable=False)
    estado = Column(String(20), default="ABIERTA", nullable=False)
    ultima_detec = Column(DateTime, default=datetime.utcnow, nullable=False)
    resuelta_en = Column(DateTime, nullable=True)
    resuelta_por = Column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=True)
    nota = Column(Text, nullable=True)

    # Relationships
    empresa = relationship("Empresa")
    almacen = relationship("Almacen")
    cristal = relationship("CatalogItem")
    usuario_resolvio = relationship("Usuario")
