from pydantic import BaseModel

class Item(BaseModel):
    text: str = None
    conf_rate: float = 0.0
    
class Ingredient(BaseModel):
    text: str = None
    conf_rate: float = 0.0