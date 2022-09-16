from typing import Union, Tuple

from pydantic import BaseModel


class CarBase(BaseModel):
    id: int


class CarCreate(CarBase):
    model: str
    owner: Tuple[int, int]
    mileage: int


class Car(CarBase):
    model: Union[str, None] = None
    owner: Union[Tuple[int, int], None] = None
    mileage: Union[int, None] = None

    class Config:
        orm_mode = True
