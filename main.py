#import uvicorn

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import init_db, get_session
from app.models import Car
from app.endpoints import crud

app = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.get("/car/{id}", response_model=Car)
async def get_car(id: str, session: AsyncSession = Depends(get_session)):
    db_car = await crud.get_car(session, car_id=id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="NOT FOUND")
    return db_car


@app.get("/car", response_model=list[Car])
async def get_cars(page: int = 0, per_page: int = 10, session: AsyncSession = Depends(get_session)):
    cars = await crud.get_cars(session, page=page, per_page=per_page)
    if cars is None:
        raise HTTPException(status_code=404, detail="NOT FOUND")
    return cars


@app.post("/car", response_model=Car)
async def post_car(car: Car, session: AsyncSession = Depends(get_session)):
    db_car = await crud.get_car(session, car_id=car.id)
    if db_car:
        return await crud.update_car(session, Car(id=car.id))
    else:
        db_car = await crud.create_car(session, car)
    if db_car is None:
        raise HTTPException(status_code=503, detail="SERVICE UNAVAILABLE")
    else:
        return db_car


@app.put("/car", response_model=Car)
async def update_car(car: Car, session: AsyncSession = Depends(get_session)):
    db_car = await crud.update_car(session, car)
    if db_car is None:
        raise HTTPException(status_code=404, detail="NOT FOUND")
    return db_car


@app.delete("/car", response_model=Car)
async def delete_car(car: Car, session: AsyncSession = Depends(get_session)):
    db_car = await crud.delete_car(session, car)
    if db_car is None:
        raise HTTPException(status_code=404, detail="NOT FOUND")
    return db_car

#if __name__ == "__main__":
    #uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
