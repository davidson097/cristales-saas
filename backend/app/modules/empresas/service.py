from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import Empresa
from .schemas import EmpresaCreate, EmpresaUpdate


class EmpresaService:
    """Business logic for Empresa operations"""
    
    @staticmethod
    def create_empresa(db: Session, empresa_data: EmpresaCreate) -> Empresa:
        """Create a new empresa"""
        db_empresa = Empresa(**empresa_data.model_dump())
        db.add(db_empresa)
        db.commit()
        db.refresh(db_empresa)
        return db_empresa
    
    @staticmethod
    def get_empresa_by_id(db: Session, empresa_id: UUID) -> Optional[Empresa]:
        """Get empresa by ID"""
        return db.query(Empresa).filter(Empresa.id == empresa_id).first()
    
    @staticmethod
    def get_empresa_by_nombre(db: Session, nombre: str) -> Optional[Empresa]:
        """Get empresa by nombre"""
        return db.query(Empresa).filter(Empresa.nombre == nombre).first()
    
    @staticmethod
    def list_empresas(
        db: Session, 
        skip: int = 0, 
        limit: int = 100,
        only_active: bool = False
    ) -> List[Empresa]:
        """List all empresas with pagination"""
        query = db.query(Empresa)
        if only_active:
            query = query.filter(Empresa.estado == True)
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def update_empresa(db: Session, empresa_id: UUID, update_data: EmpresaUpdate) -> Optional[Empresa]:
        """Update an existing empresa"""
        db_empresa = EmpresaService.get_empresa_by_id(db, empresa_id)
        if not db_empresa:
            return None
        
        update_fields = update_data.model_dump(exclude_unset=True)
        for field, value in update_fields.items():
            setattr(db_empresa, field, value)
        
        db.add(db_empresa)
        db.commit()
        db.refresh(db_empresa)
        return db_empresa
    
    @staticmethod
    def delete_empresa(db: Session, empresa_id: UUID) -> bool:
        """Delete an empresa (hard delete)"""
        db_empresa = EmpresaService.get_empresa_by_id(db, empresa_id)
        if not db_empresa:
            return False
        
        db.delete(db_empresa)
        db.commit()
        return True
    
    @staticmethod
    def toggle_empresa_estado(db: Session, empresa_id: UUID) -> Optional[Empresa]:
        """Toggle empresa active/inactive state"""
        db_empresa = EmpresaService.get_empresa_by_id(db, empresa_id)
        if not db_empresa:
            return None
        
        db_empresa.estado = not db_empresa.estado
        db.add(db_empresa)
        db.commit()
        db.refresh(db_empresa)
        return db_empresa

