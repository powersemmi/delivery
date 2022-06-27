from fastapi import APIRouter

router = APIRouter(prefix="/delivery")


@router.get("/")
async def transportation_calculation(weight: float, volume: float):
    return "OK"
