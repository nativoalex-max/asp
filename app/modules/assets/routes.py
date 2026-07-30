from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user
from app.database.deps import get_db
from app.models.user import User

from app.modules.clients.service import get_client_by_id

from app.modules.assets.schema import (
    AssetCreate,
    AssetResponse,
    AssetDrawerResponse,
    AssetUpdate,
)

from app.modules.assets.service import (
    create_asset,
    delete_asset,
    get_asset_by_id,
    get_asset_by_ip,
    get_asset_drawer,
    get_assets,
    update_asset,
)

router = APIRouter(
    prefix="/assets",
    tags=["Assets"],
)


# ==========================================================
# LIST
# ==========================================================

@router.get(
    "/",
    response_model=list[AssetResponse],
)
def list_assets(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return get_assets(db)


# ==========================================================
# DETAIL (API)
# ==========================================================

@router.get(
    "/{asset_id}",
    response_model=AssetResponse,
)
def get_asset(
    asset_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    asset = get_asset_by_id(db, asset_id)

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activo no encontrado",
        )

    return asset


# ==========================================================
# DETAIL (WEB)
# ==========================================================

@router.get(
    "/view/{asset_id}",
)
def get_asset_view(
    asset_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    asset = get_asset_by_id(db, asset_id)

    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activo no encontrado",
        )

    return JSONResponse(
        content=AssetResponse.model_validate(asset).model_dump(mode="json")
    )


@router.get(
    "/drawer/{asset_id}",
    response_model=AssetDrawerResponse,
)
def get_asset_drawer_view(
    asset_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    drawer_data = get_asset_drawer(db, asset_id)

    if not drawer_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activo no encontrado",
        )

    return drawer_data


# ==========================================================
# CREATE
# ==========================================================

@router.post(
    "/",
    response_model=AssetResponse,
    status_code=status.HTTP_201_CREATED,
)
def new_asset(
    asset: AssetCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if not get_client_by_id(db, asset.client_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado",
        )

    if get_asset_by_ip(db, asset.ip_address):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un activo con esa IP",
        )

    return create_asset(db, asset)


# ==========================================================
# UPDATE
# ==========================================================

@router.put(
    "/{asset_id}",
    response_model=AssetResponse,
)
def edit_asset(
    asset_id: UUID,
    asset: AssetUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_asset = get_asset_by_id(db, asset_id)

    if not db_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activo no encontrado",
        )

    if asset.ip_address:
        existing = get_asset_by_ip(db, asset.ip_address)

        if existing and existing.id != db_asset.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un activo con esa IP",
            )

    return update_asset(
        db,
        db_asset,
        asset,
    )


# ==========================================================
# DELETE
# ==========================================================

@router.delete(
    "/{asset_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_asset(
    asset_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_asset = get_asset_by_id(db, asset_id)

    if not db_asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activo no encontrado",
        )

    delete_asset(
        db,
        db_asset,
    )
