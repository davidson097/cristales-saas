from fastapi import APIRouter
router = APIRouter()

@router.get("/catalogo")
def list_items():
    return []
