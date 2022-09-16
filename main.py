import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from endpoints import crud
from core.database import SessionLocal
from schemas import CarSchema

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.get("/car/{id}")
async def get_car(id: int, db: Session = Depends(get_db)):
    db_car = crud.get_car(db, car_id=id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="NOT FOUND")
    return db_car


@app.get("/car")
async def get_cars(page: int = 0, per_page: int = 10, db: Session = Depends(get_db)):
    cars = crud.get_cars(db, page=page, per_page=per_page)
    return cars


@app.post("/car")
async def post_car(car: CarSchema.CarCreate, db: Session = Depends(get_db)):
    db_car = crud.get_car(db, car_id=car.id)
    if db_car:
        return crud.update_car(db, CarSchema.Car(id=car.id))
    else:
        return crud.create_car(db, car)


@app.put("/car")
async def update_car(car: CarSchema.Car, db: Session = Depends(get_db)):
    db_car = crud.update_car(db, car)
    if db_car is None:
        raise HTTPException(status_code=404, detail="NOT FOUND")
    return db_car


@app.delete("/car")
async def delete_car(car: CarSchema.Car, db: Session = Depends(get_db)):
    db_car = crud.delete_car(db, car)
    if db_car is None:
        raise HTTPException(status_code=404, detail="NOT FOUND")
    return db_car


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
