from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from delivery.settings import settings

engine = create_async_engine(
    make_url(settings.DB_URL).set(drivername="postgresql+asyncpg"),
    echo=settings.DEBUG,
    pool_pre_ping=True,
)

async_session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    async with async_session() as session:  # type: AsyncSession
        yield session
