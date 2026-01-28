from fastapi import APIRouter
router = APIRouter()

@router.get("/inventario")
def list_stock():
    return []
