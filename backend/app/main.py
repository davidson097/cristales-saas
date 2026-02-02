from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.modules.catalogo.router import router as catalogo_router
from app.modules.clientes.router import router as clientes_router
from app.modules.comisiones.router import router as comisiones_router
from app.modules.empresas.router import router as empresas_router
from app.modules.facturacion.router import router as facturacion_router
from app.modules.inventario.router import router as inventario_router
from app.modules.ordenes.router import router as ordenes_router
from app.modules.pagos.router import router as pagos_router
from app.modules.perfiles.router import router as perfiles_router
from app.modules.reportes.router import router as reportes_router
from app.modules.usuarios.router import router as usuarios_router
from app.modules.vehiculos.router import router as vehiculos_router
from app.modules.zonas.router import router as zonas_router
from app.rbac.router import router as rbac_router

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

