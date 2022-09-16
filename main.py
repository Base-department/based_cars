import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Tuple, Union


class Car(BaseModel):
    number: str
    model: Union[str, None] = None
    owner: Union[Tuple[int, int], None] = None
    mileage: Union[int, None] = None


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello"}


@app.get("/car/{id}")
async def get_car(id: int):
    return {"Car": id}


@app.get("/car")
async def get_cars(page: int, per_page: int):
    return {"All_cars": "Succ",
            "Page_number": page,
            "Cars_per_page": per_page}


@app.post("/car")
async def post_car(car: Car):
    return car


@app.put("/car")
async def update_car(car: Car):
    return car


@app.delete("/car")
async def delete_car(car: Car):
    return car


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True)
