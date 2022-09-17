from starlette.config import Config

config = Config(".env")

DATABASE_URL = config("DATABASE_URL", cast=str, default="postgresql+asyncpg://user:password@db:5432/cars")
