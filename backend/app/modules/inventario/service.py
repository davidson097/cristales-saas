from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select, and_
from .models import Almacen, StockConfig, MovimientoInventario, AlertaStock
from .schemas import (
    AlmacenCreate, AlmacenUpdate,
    StockConfigCreate, StockConfigUpdate,
    MovimientoInventarioCreate,
    AlertaStockCreate, AlertaStockUpdate
)


class AlmacenService:
    """Business logic for Almacen operations"""

    @staticmethod
    def create_almacen(db: Session, almacen_data: AlmacenCreate) -> Almacen:
        """Create a new almacen"""
        db_almacen = Almacen(**almacen_data.model_dump())
        db.add(db_almacen)
        db.commit()
        db.refresh(db_almacen)
        return db_almacen

    @staticmethod
    def get_almacen_by_id(db: Session, almacen_id: UUID) -> Optional[Almacen]:
        """Get almacen by ID"""
        return db.query(Almacen).filter(Almacen.id == almacen_id).first()

    @staticmethod
    def list_almacenes(
        db: Session,
        empresa_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 100,
        only_active: bool = True
    ) -> List[Almacen]:
        """List almacenes with optional filtering"""
        query = db.query(Almacen)
        if empresa_id:
            query = query.filter(Almacen.empresa_id == empresa_id)
        if only_active:
            query = query.filter(Almacen.activo == True)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_almacen(db: Session, almacen_id: UUID, update_data: AlmacenUpdate) -> Optional[Almacen]:
        """Update an existing almacen"""
        db_almacen = AlmacenService.get_almacen_by_id(db, almacen_id)
        if not db_almacen:
            return None

        update_fields = update_data.model_dump(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(db_almacen, field, value)

        db.add(db_almacen)
        db.commit()
        db.refresh(db_almacen)
        return db_almacen

    @staticmethod
    def delete_almacen(db: Session, almacen_id: UUID) -> bool:
        """Delete an almacen"""
        db_almacen = AlmacenService.get_almacen_by_id(db, almacen_id)
        if not db_almacen:
            return False

        db.delete(db_almacen)
        db.commit()
        return True


class StockConfigService:
    """Business logic for StockConfig operations"""

    @staticmethod
    def create_stock_config(db: Session, config_data: StockConfigCreate) -> StockConfig:
        """Create a new stock configuration"""
        db_config = StockConfig(**config_data.model_dump())
        db.add(db_config)
        db.commit()
        db.refresh(db_config)
        return db_config

    @staticmethod
    def get_stock_config_by_id(db: Session, config_id: UUID) -> Optional[StockConfig]:
        """Get stock config by ID"""
        return db.query(StockConfig).filter(StockConfig.id == config_id).first()

    @staticmethod
    def get_stock_config(db: Session, empresa_id: UUID, almacen_id: UUID, cristal_id: UUID) -> Optional[StockConfig]:
        """Get stock config by empresa, almacen, cristal"""
        return db.query(StockConfig).filter(
            and_(
                StockConfig.empresa_id == empresa_id,
                StockConfig.almacen_id == almacen_id,
                StockConfig.cristal_id == cristal_id
            )
        ).first()

    @staticmethod
    def list_stock_configs(
        db: Session,
        empresa_id: Optional[UUID] = None,
        almacen_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[StockConfig]:
        """List stock configurations"""
        query = db.query(StockConfig)
        if empresa_id:
            query = query.filter(StockConfig.empresa_id == empresa_id)
        if almacen_id:
            query = query.filter(StockConfig.almacen_id == almacen_id)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_stock_config(db: Session, config_id: UUID, update_data: StockConfigUpdate) -> Optional[StockConfig]:
        """Update stock configuration"""
        db_config = StockConfigService.get_stock_config_by_id(db, config_id)
        if not db_config:
            return None

        update_fields = update_data.model_dump(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(db_config, field, value)

        db.add(db_config)
        db.commit()
        db.refresh(db_config)
        return db_config


class MovimientoInventarioService:
    """Business logic for MovimientoInventario operations"""

    @staticmethod
    def create_movimiento(db: Session, movimiento_data: MovimientoInventarioCreate) -> MovimientoInventario:
        """Create a new inventory movement"""
        db_movimiento = MovimientoInventario(**movimiento_data.model_dump())
        db.add(db_movimiento)
        db.commit()
        db.refresh(db_movimiento)
        return db_movimiento

    @staticmethod
    def get_movimiento_by_id(db: Session, movimiento_id: UUID) -> Optional[MovimientoInventario]:
        """Get movement by ID"""
        return db.query(MovimientoInventario).filter(MovimientoInventario.id == movimiento_id).first()

    @staticmethod
    def list_movimientos(
        db: Session,
        empresa_id: Optional[UUID] = None,
        almacen_id: Optional[UUID] = None,
        cristal_id: Optional[UUID] = None,
        tipo: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[MovimientoInventario]:
        """List inventory movements with filtering"""
        query = db.query(MovimientoInventario)
        if empresa_id:
            query = query.filter(MovimientoInventario.empresa_id == empresa_id)
        if almacen_id:
            query = query.filter(MovimientoInventario.almacen_id == almacen_id)
        if cristal_id:
            query = query.filter(MovimientoInventario.cristal_id == cristal_id)
        if tipo:
            query = query.filter(MovimientoInventario.tipo == tipo)
        return query.order_by(MovimientoInventario.creado_en.desc()).offset(skip).limit(limit).all()


class AlertaStockService:
    """Business logic for AlertaStock operations"""

    @staticmethod
    def create_alerta(db: Session, alerta_data: AlertaStockCreate) -> AlertaStock:
        """Create a new stock alert"""
        db_alerta = AlertaStock(**alerta_data.model_dump())
        db.add(db_alerta)
        db.commit()
        db.refresh(db_alerta)
        return db_alerta

    @staticmethod
    def get_alerta_by_id(db: Session, alerta_id: UUID) -> Optional[AlertaStock]:
        """Get alert by ID"""
        return db.query(AlertaStock).filter(AlertaStock.id == alerta_id).first()

    @staticmethod
    def list_alertas(
        db: Session,
        empresa_id: Optional[UUID] = None,
        almacen_id: Optional[UUID] = None,
        estado: Optional[str] = None,
        severidad: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[AlertaStock]:
        """List stock alerts with filtering"""
        query = db.query(AlertaStock)
        if empresa_id:
            query = query.filter(AlertaStock.empresa_id == empresa_id)
        if almacen_id:
            query = query.filter(AlertaStock.almacen_id == almacen_id)
        if estado:
            query = query.filter(AlertaStock.estado == estado)
        if severidad:
            query = query.filter(AlertaStock.severidad == severidad)
        return query.order_by(AlertaStock.ultima_detec.desc()).offset(skip).limit(limit).all()

    @staticmethod
    def update_alerta(db: Session, alerta_id: UUID, update_data: AlertaStockUpdate) -> Optional[AlertaStock]:
        """Update stock alert"""
        db_alerta = AlertaStockService.get_alerta_by_id(db, alerta_id)
        if not db_alerta:
            return None

        update_fields = update_data.model_dump(exclude_unset=True)
        for field, value in update_fields.items():
            if field == "resuelta_por" and value:
                from datetime import datetime
                db_alerta.resuelta_en = datetime.utcnow()
            setattr(db_alerta, field, value)

        db.add(db_alerta)
        db.commit()
        db.refresh(db_alerta)
        return db_alerta

    @staticmethod
    def resolve_alerta(db: Session, alerta_id: UUID, resolved_by: UUID) -> Optional[AlertaStock]:
        """Mark alert as resolved"""
        return AlertaStockService.update_alerta(
            db, alerta_id,
            AlertaStockUpdate(estado="RESUELTA", resuelta_por=resolved_by)
        )
