from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from ...db.session import get_db
from .models import Empresa
from .schemas import EmpresaCreate, EmpresaUpdate, EmpresaRead
from .service import EmpresaService

router = APIRouter(prefix="/empresas", tags=["empresas"])


@router.post("/", response_model=EmpresaRead, status_code=status.HTTP_201_CREATED)
def create_empresa(
    empresa: EmpresaCreate,
    db: Session = Depends(get_db)
):
    """Create a new empresa"""
    # Check if empresa with same nombre already exists
    existing = EmpresaService.get_empresa_by_nombre(db, empresa.nombre)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Empresa with nombre '{empresa.nombre}' already exists"
        )
    
    db_empresa = EmpresaService.create_empresa(db, empresa)
    return db_empresa


@router.get("/", response_model=List[EmpresaRead])
def list_empresas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    only_active: bool = Query(False),
    db: Session = Depends(get_db)
):
    """List all empresas with pagination"""
    empresas = EmpresaService.list_empresas(
        db, 
        skip=skip, 
        limit=limit,
        only_active=only_active
    )
    return empresas


@router.get("/{empresa_id}", response_model=EmpresaRead)
def get_empresa(
    empresa_id: UUID,
    db: Session = Depends(get_db)
):
    """Get a specific empresa by ID"""
    db_empresa = EmpresaService.get_empresa_by_id(db, empresa_id)
    if not db_empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empresa with id {empresa_id} not found"
        )
    return db_empresa


@router.patch("/{empresa_id}", response_model=EmpresaRead)
def update_empresa(
    empresa_id: UUID,
    empresa_update: EmpresaUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing empresa"""
    db_empresa = EmpresaService.update_empresa(db, empresa_id, empresa_update)
    if not db_empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empresa with id {empresa_id} not found"
        )
    return db_empresa


@router.patch("/{empresa_id}/toggle-estado", response_model=EmpresaRead)
def toggle_empresa_estado(
    empresa_id: UUID,
    db: Session = Depends(get_db)
):
    """Toggle empresa active/inactive state"""
    db_empresa = EmpresaService.toggle_empresa_estado(db, empresa_id)
    if not db_empresa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empresa with id {empresa_id} not found"
        )
    return db_empresa


@router.delete("/{empresa_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_empresa(
    empresa_id: UUID,
    db: Session = Depends(get_db)
):
    """Delete an empresa"""
    success = EmpresaService.delete_empresa(db, empresa_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Empresa with id {empresa_id} not found"
        )
    return None

