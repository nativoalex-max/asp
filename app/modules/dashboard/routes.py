from fastapi import APIRouter

from app.modules.dashboard.service import DashboardService

router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"],
)

service = DashboardService()


@router.get("/summary")
def dashboard_summary():
    """
    Resumen general del estado de la plataforma.
    """

    return service.get_statistics()
