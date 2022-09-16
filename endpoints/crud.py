from sqlalchemy.orm import Session

from schemas import CarSchema
from models import CarDBmodel


def get_car(db: Session, car_id: int):
    try:
        return db.query(CarDBmodel.Car).filter(CarDBmodel.Car.id == car_id).first()
    except:
        return None


def get_cars(db: Session, page: int = 0, per_page: int = 10):
    try:
        return db.query(CarDBmodel.Car).offset(per_page * page).limit(per_page).all()
    except:
        return None


def create_car(db: Session, car: CarSchema.CarCreate):
    try:
        owner = str(car.owner[0]) + '-' + str(car.owner[1])
        db_car = CarDBmodel.Car(id=car.id, model=car.model, owner=owner, mileage=car.mileage)
        db.add(db_car)
        db.commit()
        db.refresh(db_car)
        return db_car
    except:
        return None


def delete_car(db: Session, car: CarSchema.Car):
    try:
        car = db.query(CarDBmodel.Car).filter(CarDBmodel.Car.id == car.id).first()
        if car:
            db.delete(car)
            db.commit()
        return car
    except:
        return None


def update_car(db: Session, car: CarSchema.Car):
    try:
        db_car = db.query(CarDBmodel.Car).filter(CarDBmodel.Car.id == car.id).first()
        if db_car:
            db_car.model = car.model
            db_car.owner = car.owner
            db_car.mileage = car.mileage
            db.commit()
        return db_car
    except:
        return None
