from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Car


async def get_car(session: AsyncSession, car_id: str):
    try:
        q = select(Car).filter(Car.id == car_id)
        result = await session.execute(q)
        result = result.first()[0]
        return result
    except:
        return None


async def get_cars(session: AsyncSession, page: int = 0, per_page: int = 10):
    try:
        q = select(Car).offset(per_page * page).limit(per_page)
        result = await session.execute(q)
        result = [res[0] for res in result.all()]
        print("--------------------------------------------")
        print(result)
        print("--------------------------------------------")
        return result
    except:
        return None


async def create_car(session: AsyncSession, car: Car):
    try:
        db_car = Car(id=car.id, model=car.model, owner=car.owner, mileage=car.mileage)
        session.add(db_car)
        await session.commit()
        return db_car
    except:
        return None


async def delete_car(session: AsyncSession, car: Car):
    try:
        q = select(Car).filter(Car.id == car.id)
        db_car = await session.execute(q)
        db_car = db_car.first()[0]
        if db_car:
            await session.delete(db_car)
            await session.commit()
        return car
    except:
        return None


async def update_car(session: AsyncSession, car: Car):
    try:
        q = select(Car).filter(Car.id == car.id)
        db_car = await session.execute(q)
        db_car = db_car.first()[0]
        if db_car:
            db_car.model = car.model if car.model else db_car.model
            db_car.owner = car.owner if car.owner else db_car.owner
            db_car.mileage = car.mileage if car.mileage else db_car.mileage
            await session.commit()
        return db_car
    except:
        return None
