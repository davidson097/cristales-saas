from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class EmpresaBase(BaseModel):
    """Base schema with common fields"""
    nombre: str = Field(..., min_length=1, max_length=255)
    razon_social: Optional[str] = Field(None, max_length=255)
    rfc: Optional[str] = Field(None, max_length=13)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = None
    ciudad: Optional[str] = Field(None, max_length=100)
    pais: Optional[str] = Field(default="Mexico", max_length=100)
    descripcion: Optional[str] = None


class EmpresaCreate(EmpresaBase):
    """Schema for creating a new empresa"""
    pass


class EmpresaUpdate(BaseModel):
    """Schema for updating empresa (all fields optional)"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=255)
    razon_social: Optional[str] = Field(None, max_length=255)
    rfc: Optional[str] = Field(None, max_length=13)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = None
    ciudad: Optional[str] = Field(None, max_length=100)
    pais: Optional[str] = Field(None, max_length=100)
    descripcion: Optional[str] = None
    estado: Optional[bool] = None


class EmpresaRead(EmpresaBase):
    """Schema for reading empresa (response)"""
    id: UUID
    estado: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
