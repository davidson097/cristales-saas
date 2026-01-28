from fastapi import APIRouter
router = APIRouter()

@router.get("/vehiculos")
def list_vehiculos():
    return []
