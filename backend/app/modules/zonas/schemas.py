from pydantic import BaseModel

class ZonaSchema(BaseModel):
    id: int
    name: str
