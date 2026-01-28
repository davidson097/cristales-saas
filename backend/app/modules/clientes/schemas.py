from pydantic import BaseModel

class ClienteSchema(BaseModel):
    id: int
    name: str
