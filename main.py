from app.core.database import init_db, get_session
from app.models import Car
from app.endpoints import crud

from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    """Database initialization before the application starts up"""
    init_db()


@app.get("/")
async def root():
    """Just check function"""
    return {"message": "Hello"}


@app.get("/car/{id}", response_model=Car)
async def get_car(id: str, session: AsyncSession = Depends(get_session)):
    """Gets information about the car by the given id from the database using the corresponding function from crud.py.

    Args:
      id: The car's number.
      session: The current session.

    Returns:
      Info about the car with the given id.

    Raises:
      HTTPException: If the car is not found.
    """
    db_car = await crud.get_car(session, car_id=id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="NOT FOUND")
    return db_car


@app.get("/car", response_model=list[Car])
async def get_cars(response: Response, page: int = 1, per_page: int = 10, session: AsyncSession = Depends(get_session)):
    """Gets information about all cars from the database using the corresponding function from crud.py, taking into account pagination from query-parameters.

    Args:
      response: Incoming response.
      page: The pagination parameter.
      per_page: The pagination parameter.
      session: The current session.

    Returns:
      Info about the cars with the given parameters.

    Raises:
      HTTPException: If the cars are not found.
    """
    cars, total_count = await crud.get_cars(session, page=page, per_page=per_page)
    response.headers["x-total-count"] = str(total_count)
    if cars is None:
        raise HTTPException(status_code=404, detail="NOT FOUND")
    return cars


@app.post("/car", response_model=Car)
async def post_car(car: Car, session: AsyncSession = Depends(get_session)):
    """Stores information about the car in the database using the corresponding function from crud.py.
    If the car is already in the database, then replaces it.

    Args:
      car: The object to POST.
      session: The current session.

    Returns:
      Info about the car to be posted.

    Raises:
      HTTPException: If the car could not be posted.
    """
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
    """Updates the car in the database using the corresponding function from crud.py.

    Args:
      car: The object to UPDATE.
      session: The current session.

    Returns:
      Info about the car to be updated.

    Raises:
      HTTPException: If the car is not found.
    """
    db_car = await crud.update_car(session, car)
    if db_car is None:
        raise HTTPException(status_code=404, detail="NOT FOUND")
    return db_car


@app.delete("/car/{id}", response_model=Car)
async def delete_car(id: str, session: AsyncSession = Depends(get_session)):
    """Deletes the car by the given id in the database using the corresponding function from crud.py.

    Args:
      id: The car's id to DELETE.
      session: The current session.

    Returns:
      Info about the car to be deleted.

    Raises:
      HTTPException: If the car is not found.
    """
    db_car = await crud.delete_car(session, id)

    if db_car is None:
        raise HTTPException(status_code=404, detail="NOT FOUND")
    return db_car

# if __name__ == "__main__":
    # uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
