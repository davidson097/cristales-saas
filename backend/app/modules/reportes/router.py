from fastapi import APIRouter
router = APIRouter()

@router.get("/reportes")
def list_reportes():
    return []
