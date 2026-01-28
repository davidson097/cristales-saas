from pydantic import BaseModel

class UsuarioSchema(BaseModel):
    id: int
    username: str
