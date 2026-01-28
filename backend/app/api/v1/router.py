from fastapi import APIRouter
from app.api.v1.health import router as health_router
from app.auth.router import router as auth_router
from app.rbac.router import router as rbac_router
from app.modules.empresas.router import router as empresas_router
from app.modules.usuarios.router import router as usuarios_router
from app.modules.perfiles.router import router as perfiles_router
from app.modules.zonas.router import router as zonas_router
from app.modules.clientes.router import router as clientes_router
from app.modules.vehiculos.router import router as vehiculos_router
from app.modules.catalogo.router import router as catalogo_router
from app.modules.inventario.router import router as inventario_router
from app.modules.ordenes.router import router as ordenes_router
from app.modules.facturacion.router import router as facturacion_router
from app.modules.pagos.router import router as pagos_router
from app.modules.comisiones.router import router as comisiones_router
from app.modules.reportes.router import router as reportes_router

api_router = APIRouter()

# Include health/diagnostics
api_router.include_router(health_router, tags=["health"])

# Include all module routers
api_router.include_router(auth_router, tags=["auth"])
api_router.include_router(rbac_router, tags=["rbac"])
api_router.include_router(empresas_router, tags=["empresas"])
api_router.include_router(usuarios_router, tags=["usuarios"])
api_router.include_router(perfiles_router, tags=["perfiles"])
api_router.include_router(zonas_router, tags=["zonas"])
api_router.include_router(clientes_router, tags=["clientes"])
api_router.include_router(vehiculos_router, tags=["vehiculos"])
api_router.include_router(catalogo_router, tags=["catalogo"])
api_router.include_router(inventario_router, tags=["inventario"])
api_router.include_router(ordenes_router, tags=["ordenes"])
api_router.include_router(facturacion_router, tags=["facturacion"])
api_router.include_router(pagos_router, tags=["pagos"])
api_router.include_router(comisiones_router, tags=["comisiones"])
api_router.include_router(reportes_router, tags=["reportes"])
