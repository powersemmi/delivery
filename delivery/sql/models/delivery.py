from sqlalchemy import Boolean, Column, Enum, Numeric, String

from delivery.models.common import AvailableCitiesEnum
from delivery.sql.models.base import BaseModel


class Delivery(BaseModel):
    __tablename__ = "delivers"

    name = Column(String(255))
    in_ = Column(Enum(AvailableCitiesEnum))
    out = Column(Enum(AvailableCitiesEnum))
    price = Column(Numeric)
    min_price = Column(Numeric)
    weight = Column(Numeric)
    volume = Column(Numeric)
    delivery_date = Column(Numeric)
    less = Column(Boolean)
    weight_multiplier = Column(Boolean)
    volume_multiplier = Column(Boolean)
