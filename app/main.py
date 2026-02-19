from app.modules.inventario.router import router as inventario_router

app.include_router(inventario_router, prefix="/inventario", tags=["inventario"])
