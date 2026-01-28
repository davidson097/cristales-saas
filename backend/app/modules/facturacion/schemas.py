from pydantic import BaseModel

class FacturaSchema(BaseModel):
    id: int
    total: int
