from pydantic import BaseModel


class Ping(BaseModel):
    msg: str
