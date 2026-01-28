from fastapi import APIRouter
router = APIRouter()

@router.get("/comisiones")
def list_comisiones():
    return []
