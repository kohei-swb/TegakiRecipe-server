from pydantic import BaseModel

class Item(BaseModel):
    text: str = None
    conf_rate: float = 0.0