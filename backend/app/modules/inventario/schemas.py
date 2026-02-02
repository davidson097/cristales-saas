from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class AlmacenBase(BaseModel):
    nombre: str
    zona_id: Optional[UUID] = None
    activo: bool = True


class AlmacenCreate(AlmacenBase):
    empresa_id: UUID


class AlmacenUpdate(BaseModel):
    nombre: Optional[str] = None
    zona_id: Optional[UUID] = None
    activo: Optional[bool] = None


class AlmacenRead(AlmacenBase):
    id: UUID
    empresa_id: UUID

    class Config:
        from_attributes = True


class StockConfigBase(BaseModel):
    stock_min: int = 0


class StockConfigCreate(StockConfigBase):
    empresa_id: UUID
    almacen_id: UUID
    cristal_id: UUID


class StockConfigUpdate(BaseModel):
    stock_min: Optional[int] = None


class StockConfigRead(StockConfigBase):
    id: UUID
    empresa_id: UUID
    almacen_id: UUID
    cristal_id: UUID

    class Config:
        from_attributes = True


class MovimientoInventarioBase(BaseModel):
    tipo: str
    cantidad: int
    costo_unit: Optional[float] = None
    ref_tipo: Optional[str] = None
    ref_id: Optional[UUID] = None
    nota: Optional[str] = None


class MovimientoInventarioCreate(MovimientoInventarioBase):
    empresa_id: UUID
    almacen_id: UUID
    cristal_id: UUID
    tramo_id: Optional[UUID] = None
    creado_por: Optional[UUID] = None


class MovimientoInventarioRead(MovimientoInventarioBase):
    id: UUID
    empresa_id: UUID
    almacen_id: UUID
    cristal_id: UUID
    tramo_id: Optional[UUID] = None
    creado_en: datetime
    creado_por: Optional[UUID] = None

    class Config:
        from_attributes = True


class AlertaStockBase(BaseModel):
    stock_min: int = 0
    stock_actual: int = 0
    severidad: str = "WARNING"
    estado: str = "ABIERTA"
    nota: Optional[str] = None


class AlertaStockCreate(AlertaStockBase):
    empresa_id: UUID
    almacen_id: UUID
    cristal_id: UUID


class AlertaStockUpdate(BaseModel):
    stock_min: Optional[int] = None
    stock_actual: Optional[int] = None
    severidad: Optional[str] = None
    estado: Optional[str] = None
    resuelta_por: Optional[UUID] = None
    nota: Optional[str] = None


class AlertaStockRead(AlertaStockBase):
    id: UUID
    empresa_id: UUID
    almacen_id: UUID
    cristal_id: UUID
    ultima_detec: datetime
    resuelta_en: Optional[datetime] = None
    resuelta_por: Optional[UUID] = None

    class Config:
        from_attributes = True
