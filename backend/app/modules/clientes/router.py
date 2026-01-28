from fastapi import APIRouter
router = APIRouter()

@router.get("/clientes")
def list_clientes():
    return []
