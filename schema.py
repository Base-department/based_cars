# build a schema using pydantic
from pydantic import BaseModel
from typing import Union, Tuple


class Car(BaseModel):
    number: str
    model: Union[str, None] = None
    owner: Union[Tuple[int, int], None] = None
    mileage: Union[int, None] = None

    class Config:
        orm_mode = True
