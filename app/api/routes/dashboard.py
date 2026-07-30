from uuid import UUID

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.core.config import settings
from app.database.deps import get_db
from app.services.system_service import get_system_info

from app.modules.assets.schema import AssetCreate
from app.modules.assets.service import create_asset, get_assets

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()


# ------------------------
# Dashboard
# ------------------------

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):

    system_info = get_system_info()

    return templates.TemplateResponse(
        request=request,
        name="dashboard/index.html",
        context={
            "request": request,
            "app_name": settings.APP_NAME,
            "description": settings.APP_DESCRIPTION,
            "version": f"{settings.APP_VERSION} {settings.APP_CODENAME}",
            "system_info": system_info,
        },
    )


# ------------------------
# Assets
# ------------------------

@router.get("/assets", response_class=HTMLResponse)
async def assets_page(
    request: Request,
    db: Session = Depends(get_db),
):

    return templates.TemplateResponse(
        request=request,
        name="assets/index.html",
        context={
            "request": request,
            "app_name": settings.APP_NAME,
            "version": f"{settings.APP_VERSION} {settings.APP_CODENAME}",
            "assets": get_assets(db),
        },
    )


@router.get("/assets/new", response_class=HTMLResponse)
async def asset_create_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="assets/create.html",
        context={
            "request": request,
            "app_name": settings.APP_NAME,
            "version": f"{settings.APP_VERSION} {settings.APP_CODENAME}",
        },
    )


@router.post("/assets/new")
async def asset_create(
    request: Request,
    db: Session = Depends(get_db),

    name: str = Form(...),
    hostname: str = Form(""),
    ip_address: str = Form(...),
    operating_system: str = Form(""),
    asset_type: str = Form(...),
    criticality: str = Form("Media"),
):

    asset = AssetCreate(

        # <<< IMPORTANTE >>>
        # Reemplaza este UUID por un client_id que YA EXISTA en tu tabla clients
        client_id=UUID("3cdbaad3-1195-4dc1-bc94-5f7a81a06fee"),

        name=name,
        hostname=hostname,
        ip_address=ip_address,
        dns_name=None,
        mac_address=None,
        operating_system=operating_system,
        os_version=None,
        manufacturer=None,
        model=None,
        asset_type=asset_type,
        environment="Producción",
        criticality=criticality,
        owner=None,
        location=None,
        description=None,
        is_active=True,
    )

    create_asset(db, asset)

    return RedirectResponse(
        "/assets",
        status_code=303,
    )
