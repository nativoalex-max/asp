from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.system import router as system_router
from app.api.routes.users import router as users_router

from app.modules.clients.routes import router as clients_router
from app.modules.assets.routes import router as assets_router

api_router = APIRouter()

api_router.include_router(dashboard_router)
api_router.include_router(system_router)

api_router.include_router(auth_router)
api_router.include_router(users_router)

api_router.include_router(clients_router)
api_router.include_router(assets_router)
