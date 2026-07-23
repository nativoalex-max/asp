from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.config import settings

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="dashboard/index.html",
        context={
            "request": request,
            "app_name": settings.APP_NAME,
            "description": settings.APP_DESCRIPTION,
            "version": f"{settings.APP_VERSION} {settings.APP_CODENAME}",
        },
    )
