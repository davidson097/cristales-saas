from fastapi import APIRouter
router = APIRouter()

@router.get("/empresas")
def list_empresas():
    return []
