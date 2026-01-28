from fastapi import APIRouter
router = APIRouter()

@router.get("/usuarios")
def list_usuarios():
    return []
