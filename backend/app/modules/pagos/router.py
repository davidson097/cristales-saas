from fastapi import APIRouter
router = APIRouter()

@router.get("/pagos")
def list_pagos():
    return []
