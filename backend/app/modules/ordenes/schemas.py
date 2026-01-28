from pydantic import BaseModel

class OrdenSchema(BaseModel):
    id: int
    description: str
