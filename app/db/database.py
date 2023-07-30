from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
from app.models import models

DATABASE_URL: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, future=True, echo=False)

Session_local_async = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def db_init() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)


async def get_db() -> AsyncSession:
    async with Session_local_async() as session:
        yield session
