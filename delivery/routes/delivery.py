import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from delivery.models.common import AvailableCitiesEnum
from delivery.procedures.delivery_calc import calc_info
from delivery.sql.db import get_db

router = APIRouter(prefix="/delivery")
logger = logging.getLogger(__name__)


@router.get("/")
async def transportation_calculation(
    weight: float,
    volume: float,
    in_: AvailableCitiesEnum,
    out: AvailableCitiesEnum,
    session: AsyncSession = Depends(get_db),
):
    res = await calc_info(
        session=session, in_=in_, out=out, weight=weight, volume=volume
    )
    logger.debug(f"{res=}")
    return res
