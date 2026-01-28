from fastapi import APIRouter
router = APIRouter()

@router.get("/zonas")
def list_zonas():
    return []
