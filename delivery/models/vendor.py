from pydantic import BaseModel

from delivery.models.common import AvailableCitiesEnum


class VendorInfo(BaseModel):
    name: str
    in_: AvailableCitiesEnum
    out: AvailableCitiesEnum
    price: int
    min_price: int
    weight: float
    volume: float
    delivery_date: int
    less: bool
    weight_multiplier: bool
    volume_multiplier: bool
