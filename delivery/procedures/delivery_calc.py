import logging

from sqlalchemy import and_, asc, func, select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from delivery.models.common import AvailableCitiesEnum
from delivery.sql.models.delivery import Delivery

logger = logging.getLogger(__name__)


async def calc_for_weight(
        session: AsyncSession,
        vendor_name: str,
        weight: float,
        volume: float,
        in_: AvailableCitiesEnum,
        out: AvailableCitiesEnum,
) -> Delivery | None:
    sql = (
        select(Delivery)
        .filter(
            and_(
                Delivery.in_ == in_,
                Delivery.out == out,
                Delivery.name == vendor_name,
                Delivery.weight > weight,
                or_(Delivery.volume > volume, Delivery.volume == None),
            )
        )
        .order_by(asc(Delivery.weight))
        .limit(1)
    )
    return (await session.execute(sql)).scalar_one_or_none()


async def calc_for_volume(
        session: AsyncSession,
        vendor_name: str,
        weight: float,
        volume: float,
        in_: AvailableCitiesEnum,
        out: AvailableCitiesEnum,
) -> Delivery | None:
    sql = (
        select(Delivery)
        .filter(
            and_(
                Delivery.in_ == in_,
                Delivery.out == out,
                Delivery.name == vendor_name,
                Delivery.volume > volume,
                or_(Delivery.weight > weight, Delivery.weight == None)
            )
        )
        .order_by(asc(Delivery.volume))
        .limit(1)
    )
    return (await session.execute(sql)).scalar_one_or_none()


async def calc_info(
        session: AsyncSession,
        in_: AvailableCitiesEnum,
        out: AvailableCitiesEnum,
        weight: float,
        volume: float,
):
    # 1) Берём все уникальные доставки и проходимся по ним циклом
    # 1.1) Считаем прайс по весу
    # 1.1.1) Cохраняем минимальный прайс по весу
    # 1.2) Считаем прайс по объём
    # 1.2.1) Cохраняем минимальный прайс по объём
    # 1.3) max(1.1, 1.1.1, 1.2, 1.2.1)
    # 2) min(из всех (1.3))

    all_vendors = [
        i[0]
        for i in (
            await session.execute(select(func.distinct(Delivery.name)))
        ).fetchall()
    ]

    res_list = []
    for vendor_name in all_vendors:

        weight_res: Delivery | None = await calc_for_weight(
            session=session,
            vendor_name=vendor_name,
            weight=weight,
            volume=volume,
            in_=in_,
            out=out,
        )

        if weight_res:
            weight_price = (
                weight_res.price * weight
                if weight_res.weight_multiplier
                else weight_res.price
            )
            weight_min_price = weight_res.min_price
        else:
            weight_price = weight_min_price = 0

        volume_res: Delivery | None = await calc_for_volume(
            session=session,
            vendor_name=vendor_name,
            weight=weight,
            volume=volume,
            in_=in_,
            out=out,
        )

        if volume_res:
            volume_price = (
                volume_res.price * volume
                if volume_res.volume_multiplier
                else volume_res.price
            )
            volume_min_price = volume_res.min_price
        else:
            volume_price = volume_min_price = 0

        if any([weight_price, weight_min_price, volume_price, volume_min_price]):
            price = max(
                weight_price,
                weight_min_price,
                volume_price,
                volume_min_price,
            )
            res = (
                weight_res
                if weight_price == price or weight_min_price == price
                else volume_res
            )
            res_list.append(
                {
                    "vendor": vendor_name,
                    "price": price,
                    "res": res,
                }
            )

    return min(res_list, key=lambda x: x["price"]) if res_list else None
