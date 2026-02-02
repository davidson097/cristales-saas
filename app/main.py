import sys
import os

# Temporarily remove the current directory from sys.path to avoid name conflicts
current_dir = os.getcwd()
if current_dir in sys.path:
    sys.path.remove(current_dir)

# Add backend directory to path
backend_path = os.path.join(current_dir, "backend")
sys.path.insert(0, backend_path)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import backend modules by importing the backend app package
import app.core.config as config_module
settings = config_module.settings

import app.modules.catalogo.router as catalogo_mod
catalogo_router = catalogo_mod.router

import app.modules.clientes.router as clientes_mod
clientes_router = clientes_mod.router

import app.modules.comisiones.router as comisiones_mod
comisiones_router = comisiones_mod.router

import app.modules.empresas.router as empresas_mod
empresas_router = empresas_mod.router

import app.modules.facturacion.router as facturacion_mod
facturacion_router = facturacion_mod.router

import app.modules.inventario.router as inventario_mod
inventario_router = inventario_mod.router

import app.modules.ordenes.router as ordenes_mod
ordenes_router = ordenes_mod.router

import app.modules.pagos.router as pagos_mod
pagos_router = pagos_mod.router

import app.modules.perfiles.router as perfiles_mod
perfiles_router = perfiles_mod.router

import app.modules.reportes.router as reportes_mod
reportes_router = reportes_mod.router

import app.modules.usuarios.router as usuarios_mod
usuarios_router = usuarios_mod.router

import app.modules.vehiculos.router as vehiculos_mod
vehiculos_router = vehiculos_mod.router

import app.modules.zonas.router as zonas_mod
zonas_router = zonas_mod.router

import app.rbac.router as rbac_mod
rbac_router = rbac_mod.router

app = FastAPI(title="Cristales SaaS API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(catalogo_router, prefix="/api/v1")
app.include_router(clientes_router, prefix="/api/v1")
app.include_router(comisiones_router, prefix="/api/v1")
app.include_router(empresas_router, prefix="/api/v1")
app.include_router(facturacion_router, prefix="/api/v1")
app.include_router(inventario_router, prefix="/api/v1")
app.include_router(ordenes_router, prefix="/api/v1")
app.include_router(pagos_router, prefix="/api/v1")
app.include_router(perfiles_router, prefix="/api/v1")
app.include_router(reportes_router, prefix="/api/v1")
app.include_router(usuarios_router, prefix="/api/v1")
app.include_router(vehiculos_router, prefix="/api/v1")
app.include_router(zonas_router, prefix="/api/v1")
app.include_router(rbac_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Cristales SaaS API", "version": "0.1.0"}
