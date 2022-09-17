from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from project.app.models import Car


async def get_car(session: AsyncSession, car_id: str):
    try:
        q = select(Car).filter(Car.id == car_id)
        result = next(await session.execute(q), None)
        return result
    except:
        return None


async def get_cars(session: AsyncSession, page: int = 0, per_page: int = 10):
    try:
        q = select(Car).offset(per_page * page).limit(per_page)
        result = await session.execute(q)
        return result
    except:
        return None


async def create_car(session: AsyncSession, car: Car):
    try:
        owner = car.owner
        db_car = Car(id=car.id, model=car.model, owner=owner, mileage=car.mileage)
        session.add(db_car)
        await session.commit()
        return db_car
    except:
        return None


async def delete_car(session: AsyncSession, car: Car):
    try:
        db_car = next(await session.execute(select(Car).filter(Car.id == car.id)), None)
        if db_car:
            await session.delete(db_car)
            await session.commit()
        return car
    except:
        return None


async def update_car(session: AsyncSession, car: Car):
    try:
        db_car = next(await session.execute(select(Car).filter(Car.id == car.id)), None)
        if db_car:
            db_car.model = car.model
            db_car.owner = car.owner
            db_car.mileage = car.mileage
            await session.commit()
        return db_car
    except:
        return None
