import asyncio
import logging
from glob import glob
from pathlib import Path

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from delivery.models.common import AvailableCitiesEnum
from delivery.models.vendor import VendorInfo
from delivery.sql.db import async_session
from delivery.sql.models.delivery import Delivery

logger = logging.getLogger(__name__)


def get_all_csv_paths() -> list[Path]:
    return [Path(i) for i in glob("./data/*/*.csv")]


def parse_data(path: Path) -> list[list[VendorInfo]]:
    logger.debug(f"Start parsing file on {path=}")
    df = pd.read_csv(path.absolute(), sep="|")
    # filter
    df = (
        df[
            df["in"].map(AvailableCitiesEnum.has_value)
            & df["out"].map(AvailableCitiesEnum.has_value)
        ]
        .reset_index()
        .drop(columns=["index"])
    )

    comp = df["comp"]
    out = df["out"]
    in_ = df["in"]
    date = df["date"]
    min_ = df["min"]

    data_columns = df.columns[5:]
    for col_name in data_columns:
        multiplier = int(col_name[0])
        less = True if col_name[1] == "<" else False
        logger.debug(f"{col_name=}")
        weight, volume = col_name[2:].replace(",", ".").split("/")

        weight = float(weight) if weight != "none" else None
        volume = float(volume) if volume != "none" else None

        new_df = pd.DataFrame()
        new_df["name"] = comp
        new_df["out"] = out.map(AvailableCitiesEnum)
        new_df["in_"] = in_.map(AvailableCitiesEnum)

        new_df["weight"] = weight
        new_df["volume"] = volume

        new_df["delivery_date"] = date.astype(int)
        new_df["min_price"] = min_.astype(int)
        if df[col_name].dtype == "O":
            new_df["price"] = df[col_name].str.replace(",", ".").astype(float)
        else:
            new_df["price"] = df[col_name]

        new_df["weight_multiplier"] = False
        new_df["volume_multiplier"] = False

        if multiplier == 1:
            new_df["weight_multiplier"] = True
        if multiplier == 2:
            new_df["volume_multiplier"] = True

        new_df["less"] = less
        yield [VendorInfo.parse_obj(i) for i in new_df.to_dict(orient="records")]


async def load_all(vendors_info: list[VendorInfo]):
    delivers = []
    for delivery in vendors_info:
        delivers.append(Delivery(**delivery.dict()))

    async with async_session() as session:  # type: AsyncSession
        session.add_all(delivers)
        await session.commit()


async def pipline():
    for data_path in get_all_csv_paths():
        for data in parse_data(data_path):
            await load_all(data)


if __name__ == "__main__":
    asyncio.run(pipline())
