from typing import Optional

from sqlmodel import SQLModel, Field


class CarBase(SQLModel):
    model: Optional[str] = None
    owner: Optional[int] = None
    mileage: Optional[int] = None


class Car(CarBase, table=True, extend_existing=True):
    __tablename__ = "Car"
    __table_args__ = {'extend_existing': True}

    id: str = Field(default=None, primary_key=True)


class CarCreate(CarBase):
    pass
