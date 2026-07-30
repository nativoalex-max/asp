from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database.deps import get_db
from app.modules.discovery.service import run_discovery

router = APIRouter(
    prefix="/discovery",
    tags=["Discovery"],
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def discovery_index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="discovery/index.html",
        context={
            "request": request,
        },
    )


@router.get("/new")
def discovery_new(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="discovery/create.html",
        context={
            "request": request,
        },
    )


@router.post("/start")
def discovery_start(
    request: Request,
    target: str = Form(...),
    profile: str = Form("quick"),
    client_id: str = Form(...),
    db: Session = Depends(get_db),
):
    try:
        result = run_discovery(
            db=db,
            target=target,
            profile=profile,
            client_id=client_id,
        )

        return templates.TemplateResponse(
            request=request,
            name="discovery/result.html",
            context={
                "request": request,
                "result": result,
            },
        )

    except Exception as ex:
        raise HTTPException(
            status_code=500,
            detail=str(ex),
        )
