from pydantic import BaseModel

class ComisionSchema(BaseModel):
    id: int
    amount: int
