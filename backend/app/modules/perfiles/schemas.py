from pydantic import BaseModel

class PerfilSchema(BaseModel):
    id: int
    name: str
