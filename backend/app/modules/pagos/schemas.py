from pydantic import BaseModel

class PagoSchema(BaseModel):
    id: int
    amount: int
