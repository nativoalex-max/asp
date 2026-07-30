from fastapi import APIRouter

from app.api.routes.auth import router as auth_router
from app.api.routes.dashboard import router as dashboard_router
from app.api.routes.system import router as system_router
from app.api.routes.users import router as users_router

from app.modules.assets.routes import router as assets_router
from app.modules.clients.routes import router as clients_router
from app.modules.dashboard.routes import router as dashboard_api_router
from app.modules.discovery.routes import router as discovery_router
from app.modules.scans.routes import router as scans_router
from app.modules.vulnerabilities.router import router as vulnerabilities_router
from app.modules.vulnerability_catalog.router import (
    router as vulnerability_catalog_router,
)

api_router = APIRouter()

# Dashboard Web
api_router.include_router(dashboard_router)

# Dashboard API
api_router.include_router(dashboard_api_router)

# Sistema
api_router.include_router(system_router)

# Autenticación
api_router.include_router(auth_router)
api_router.include_router(users_router)

# Inventario
api_router.include_router(clients_router)
api_router.include_router(assets_router)

# Discovery
api_router.include_router(discovery_router)

# Escaneos
api_router.include_router(scans_router)

# Vulnerabilidades
api_router.include_router(vulnerabilities_router)
api_router.include_router(vulnerability_catalog_router)
