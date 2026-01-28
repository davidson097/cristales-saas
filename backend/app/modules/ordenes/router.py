from fastapi import APIRouter
router = APIRouter()

@router.get("/ordenes")
def list_ordenes():
    return []
