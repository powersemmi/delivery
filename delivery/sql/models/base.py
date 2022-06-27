from datetime import datetime
from typing import Optional, TypeAlias

from sqlalchemy import TIMESTAMP, BigInteger, Column, Identity, func
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import declarative_base

Base: TypeAlias = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(BigInteger, Identity(always=True), primary_key=True, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=datetime.utcnow,
    )

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs):
        obj = cls(**kwargs)
        session.add(obj)
        await session.flush()
        return obj

    @classmethod
    async def get(cls, session: AsyncSession, _id: int) -> Optional["BaseModel"]:
        result: Result = await session.get(cls, _id)
        return result.scalar_one_or_none()
