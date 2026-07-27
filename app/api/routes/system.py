from fastapi import APIRouter

from app.services.system_service import get_system_info

router = APIRouter()


@router.get("/api/system")
async def system_info():
    return get_system_info()
