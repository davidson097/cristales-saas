from pydantic import BaseModel

class VehiculoSchema(BaseModel):
    id: int
    plate: str
