from pydantic import BaseModel

class StockSchema(BaseModel):
    id: int
    name: str
