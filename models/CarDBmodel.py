from sqlalchemy import Column, String, Integer
from core.database import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True, unique=True)
    model = Column(String)
    owner = Column(String)
    mileage = Column(Integer)
