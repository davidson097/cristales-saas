from pydantic import BaseModel

class EmpresaSchema(BaseModel):
    id: int
    name: str
