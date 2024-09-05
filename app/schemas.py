from pydantic import BaseModel, Field, constr
from typing import Optional

class Item(BaseModel):
    id: Optional[int] = Field(default=None, alias="id")
    name: constr(min_length=1) 
    price: float = Field(gt=0)  