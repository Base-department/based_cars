from typing import Optional

from sqlmodel import SQLModel, Field


class CarBase(SQLModel):
    """Pydantic model for car"""
    model: Optional[str] = None
    owner: Optional[str] = None
    mileage: Optional[int] = None


class Car(CarBase, table=True, extend_existing=True):
    """Extended pydantic model for car with an additional attribute id"""
    id: str = Field(primary_key=True)


class CarCreate(CarBase):
    pass
