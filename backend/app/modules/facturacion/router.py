from fastapi import APIRouter
router = APIRouter()

@router.get("/facturas")
def list_facturas():
    return []
