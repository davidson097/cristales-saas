from fastapi import APIRouter
router = APIRouter()

@router.get("/perfiles")
def list_perfiles():
    return []
