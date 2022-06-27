from fastapi import APIRouter, Request

from delivery.models.common import AvailableCitiesEnum
from delivery.settings import templates

router = APIRouter()


@router.get("/")
async def index(request: Request):
    countries = AvailableCitiesEnum.get_values()

    return templates.TemplateResponse(
        "index.html",
        context={"request": request, "in_": countries, "out": countries},
    )
