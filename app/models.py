from typing import Optional

from sqlmodel import SQLModel, Field


class CarBase(SQLModel):
    model: Optional[str] = None
    owner: Optional[str] = None
    mileage: Optional[int] = None


class Car(CarBase, table=True, extend_existing=True):
    id: str = Field(primary_key=True)


class CarCreate(CarBase):
    pass
