from pydantic import BaseModel

from delivery.models.common import AvailableCitiesEnum


class VendorInfo(BaseModel):
    name: str
    in_: AvailableCitiesEnum
    out: AvailableCitiesEnum
    price: float
    min_price: int
    weight: float | None
    volume: float | None
    delivery_date: int
    less: bool
    weight_multiplier: bool
    volume_multiplier: bool
