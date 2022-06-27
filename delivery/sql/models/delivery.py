from sqlalchemy import Boolean, Column, Enum, Float, Integer, String

from delivery.models.common import AvailableCitiesEnum
from delivery.sql.models.base import BaseModel


class Delivery(BaseModel):
    __tablename__ = "delivers"

    name = Column(String(255))
    in_ = Column(Enum(AvailableCitiesEnum))
    out = Column(Enum(AvailableCitiesEnum))
    price = Column(Integer)
    min_price = Column(Integer)
    weight = Column(Float)
    volume = Column(Float)
    delivery_date = Column(Integer)
    less = Column(Boolean)
    weight_multiplier = Column(Boolean)
    volume_multiplier = Column(Boolean)
