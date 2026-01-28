from pydantic import BaseModel

class CatalogItemSchema(BaseModel):
    id: int
    name: str
