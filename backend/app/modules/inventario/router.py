from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from ...db.session import get_db
from .models import Almacen, StockConfig, MovimientoInventario, AlertaStock
from .schemas import (
    AlmacenCreate, AlmacenUpdate, AlmacenRead,
    StockConfigCreate, StockConfigUpdate, StockConfigRead,
    MovimientoInventarioCreate, MovimientoInventarioRead,
    AlertaStockCreate, AlertaStockUpdate, AlertaStockRead
)
from .service import (
    AlmacenService, StockConfigService,
    MovimientoInventarioService, AlertaStockService
)

router = APIRouter(prefix="/inventario", tags=["inventario"])


# ========== ALMACENES ENDPOINTS ==========

@router.post("/almacenes/", response_model=AlmacenRead, status_code=status.HTTP_201_CREATED)
def create_almacen(
    almacen: AlmacenCreate,
    db: Session = Depends(get_db)
):
    """Create a new almacen"""
    db_almacen = AlmacenService.create_almacen(db, almacen)
    return db_almacen


@router.get("/almacenes/", response_model=List[AlmacenRead])
def list_almacenes(
    empresa_id: Optional[UUID] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    only_active: bool = Query(True),
    db: Session = Depends(get_db)
):
    """List almacenes with optional filtering"""
    almacenes = AlmacenService.list_almacenes(
        db, empresa_id=empresa_id, skip=skip, limit=limit, only_active=only_active
    )
    return almacenes


@router.get("/almacenes/{almacen_id}", response_model=AlmacenRead)
def get_almacen(
    almacen_id: UUID,
    db: Session = Depends(get_db)
):
    """Get almacen by ID"""
    db_almacen = AlmacenService.get_almacen_by_id(db, almacen_id)
    if not db_almacen:
        raise HTTPException(status_code=404, detail="Almacen not found")
    return db_almacen


@router.put("/almacenes/{almacen_id}", response_model=AlmacenRead)
def update_almacen(
    almacen_id: UUID,
    almacen_update: AlmacenUpdate,
    db: Session = Depends(get_db)
):
    """Update an almacen"""
    db_almacen = AlmacenService.update_almacen(db, almacen_id, almacen_update)
    if not db_almacen:
        raise HTTPException(status_code=404, detail="Almacen not found")
    return db_almacen


@router.delete("/almacenes/{almacen_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_almacen(
    almacen_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete an almacen"""
    success = AlmacenService.delete_almacen(db, almacen_id)
    if not success:
        raise HTTPException(status_code=404, detail="Almacen not found")


# ========== STOCK CONFIG ENDPOINTS ==========

@router.post("/stock-config/", response_model=StockConfigRead, status_code=status.HTTP_201_CREATED)
def create_stock_config(
    config: StockConfigCreate,
    db: Session = Depends(get_db)
):
    """Create stock configuration"""
    # Check if config already exists
    existing = StockConfigService.get_stock_config(
        db, config.empresa_id, config.almacen_id, config.cristal_id
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Stock config already exists for this empresa/almacen/cristal"
        )

    db_config = StockConfigService.create_stock_config(db, config)
    return db_config


@router.get("/stock-config/", response_model=List[StockConfigRead])
def list_stock_configs(
    empresa_id: Optional[UUID] = None,
    almacen_id: Optional[UUID] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """List stock configurations"""
    configs = StockConfigService.list_stock_configs(
        db, empresa_id=empresa_id, almacen_id=almacen_id, skip=skip, limit=limit
    )
    return configs


@router.get("/stock-config/{config_id}", response_model=StockConfigRead)
def get_stock_config(
    config_id: UUID,
    db: Session = Depends(get_db)
):
    """Get stock config by ID"""
    db_config = StockConfigService.get_stock_config_by_id(db, config_id)
    if not db_config:
        raise HTTPException(status_code=404, detail="Stock config not found")
    return db_config


@router.put("/stock-config/{config_id}", response_model=StockConfigRead)
def update_stock_config(
    config_id: UUID,
    config_update: StockConfigUpdate,
    db: Session = Depends(get_db)
):
    """Update stock configuration"""
    db_config = StockConfigService.update_stock_config(db, config_id, config_update)
    if not db_config:
        raise HTTPException(status_code=404, detail="Stock config not found")
    return db_config


# ========== MOVIMIENTOS INVENTARIO ENDPOINTS ==========

@router.post("/movimientos/", response_model=MovimientoInventarioRead, status_code=status.HTTP_201_CREATED)
def create_movimiento(
    movimiento: MovimientoInventarioCreate,
    db: Session = Depends(get_db)
):
    """Create inventory movement"""
    db_movimiento = MovimientoInventarioService.create_movimiento(db, movimiento)
    return db_movimiento


@router.get("/movimientos/", response_model=List[MovimientoInventarioRead])
def list_movimientos(
    empresa_id: Optional[UUID] = None,
    almacen_id: Optional[UUID] = None,
    cristal_id: Optional[UUID] = None,
    tipo: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """List inventory movements with filtering"""
    movimientos = MovimientoInventarioService.list_movimientos(
        db, empresa_id=empresa_id, almacen_id=almacen_id,
        cristal_id=cristal_id, tipo=tipo, skip=skip, limit=limit
    )
    return movimientos


@router.get("/movimientos/{movimiento_id}", response_model=MovimientoInventarioRead)
def get_movimiento(
    movimiento_id: UUID,
    db: Session = Depends(get_db)
):
    """Get movement by ID"""
    db_movimiento = MovimientoInventarioService.get_movimiento_by_id(db, movimiento_id)
    if not db_movimiento:
        raise HTTPException(status_code=404, detail="Movimiento not found")
    return db_movimiento


# ========== ALERTAS STOCK ENDPOINTS ==========

@router.post("/alertas/", response_model=AlertaStockRead, status_code=status.HTTP_201_CREATED)
def create_alerta(
    alerta: AlertaStockCreate,
    db: Session = Depends(get_db)
):
    """Create stock alert"""
    db_alerta = AlertaStockService.create_alerta(db, alerta)
    return db_alerta


@router.get("/alertas/", response_model=List[AlertaStockRead])
def list_alertas(
    empresa_id: Optional[UUID] = None,
    almacen_id: Optional[UUID] = None,
    estado: Optional[str] = None,
    severidad: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """List stock alerts with filtering"""
    alertas = AlertaStockService.list_alertas(
        db, empresa_id=empresa_id, almacen_id=almacen_id,
        estado=estado, severidad=severidad, skip=skip, limit=limit
    )
    return alertas


@router.get("/alertas/{alerta_id}", response_model=AlertaStockRead)
def get_alerta(
    alerta_id: UUID,
    db: Session = Depends(get_db)
):
    """Get alert by ID"""
    db_alerta = AlertaStockService.get_alerta_by_id(db, alerta_id)
    if not db_alerta:
        raise HTTPException(status_code=404, detail="Alerta not found")
    return db_alerta


@router.put("/alertas/{alerta_id}", response_model=AlertaStockRead)
def update_alerta(
    alerta_id: UUID,
    alerta_update: AlertaStockUpdate,
    db: Session = Depends(get_db)
):
    """Update stock alert"""
    db_alerta = AlertaStockService.update_alerta(db, alerta_id, alerta_update)
    if not db_alerta:
        raise HTTPException(status_code=404, detail="Alerta not found")
    return db_alerta


@router.post("/alertas/{alerta_id}/resolve", response_model=AlertaStockRead)
def resolve_alerta(
    alerta_id: UUID,
    resolved_by: UUID = Query(..., description="User ID who resolved the alert"),
    db: Session = Depends(get_db)
):
    """Mark alert as resolved"""
    db_alerta = AlertaStockService.resolve_alerta(db, alerta_id, resolved_by)
    if not db_alerta:
        raise HTTPException(status_code=404, detail="Alerta not found")
    return db_alerta
