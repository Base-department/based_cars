# CRUD operations implementation
from app.models import Car

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func


async def get_car(session: AsyncSession, car_id: str):
    """Gets information about the car by the given id from the database.

    Args:
      session: The current session.
      car_id: The car's number.

    Returns:
      Info about the car with the given id.
    """
    try:
        q = select(Car).filter(Car.id == car_id)
        result = await session.execute(q)
        result = result.first()[0]
        return result
    except:
        return None


async def get_cars(session: AsyncSession, page: int = 1, per_page: int = 10):
    """Gets information about all cars from the database, taking into account pagination from query-parameters.

    Args:
      session: The current session.
      page: The pagination parameter.
      per_page: The pagination parameter.

    Returns:
      Info about the cars with the given parameters.
    """
    try:
        q = select(Car).offset(per_page * (page - 1)).limit(per_page)
        q_count = func.count(Car.id)
        result = await session.execute(q)
        total_count = await session.execute(q_count)
        result = [res[0] for res in result.all()]
        return result, total_count.first()[0]
    except:
        return None


async def create_car(session: AsyncSession, car: Car):
    """Posts the car in the database.

    Args:
      session: The current session.
      car: The object to POST.

    Returns:
      Info about the car to be posted.
    """
    try:
        db_car = Car(id=car.id, model=car.model, owner=car.owner, mileage=car.mileage)
        session.add(db_car)
        await session.commit()
        return db_car
    except:
        return None


async def delete_car(session: AsyncSession, id: str):
    """Deletes the car by the given id in the database.

    Args:
      session: The current session.
      id: The car's id to DELETE.

    Returns:
      Info about the car to be deleted.
    """
    try:
        q = select(Car).filter(Car.id == id)
        db_car = await session.execute(q)
        db_car = db_car.first()[0]
        if db_car:
            await session.delete(db_car)
            await session.commit()
        return db_car
    except:
        return None


async def update_car(session: AsyncSession, car: Car):
    """Updates the car in the database.

    Args:
      session: The current session.
      car: The object to UPDATE.

    Returns:
      Info about the car to be updated.
    """
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
