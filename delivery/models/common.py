from enum import Enum


class AvailableCitiesEnum(Enum):
    Moscow = "Москва"
    SaintPetersburg = "Санкт Петербург"
    Novosibirsk = "Новосибирск"
    Yekaterinburg = "Екатеринбург"
    Kazan = "Казань"
    NizhnyNovgorod = "Нижний Новгород"
    Chelyabinsk = "Челябинск"
    Omsk = "Омск"
    Krasnoyarsk = "Красноярск"
    Irkutsk = "Иркутск"
    Vladivostok = "Владивосток"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def get_values(cls):
        return [e.value for e in cls]
