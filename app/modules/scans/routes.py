"""Rutas HTTP para operaciones del modulo Scans."""

from uuid import UUID
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user
from app.database.deps import get_db
from app.models.user import User

from app.modules.scans.schema import (
    ScanRunRequest,
    ScanResponse,
)

from app.modules.scans.service import (
    run_scan,
    get_scan,
    list_scans,
    delete_scan,
)

router = APIRouter(
    prefix="/scans",
    tags=["Scans"],
)


@router.get(
    "/",
    response_model=list[ScanResponse],
)
def scans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> list[ScanResponse]:
    """Listar scans disponibles.

    Args:
        db: Sesion activa de SQLAlchemy.
        current_user: Usuario autenticado.

    Returns:
        Lista de scans serializados.
    """
    return list_scans(db)


@router.get(
    "/{scan_id}",
    response_model=ScanResponse,
)
def scan(
    scan_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> ScanResponse:
    """Obtener un scan por identificador.

    Args:
        scan_id: Identificador unico del scan.
        db: Sesion activa de SQLAlchemy.
        current_user: Usuario autenticado.

    Returns:
        Scan serializado.
    """
    db_scan = get_scan(db, scan_id)

    if not db_scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Escaneo no encontrado",
        )

    return db_scan


@router.post(
    "/run",
    status_code=status.HTTP_201_CREATED,
)
def execute_scan(
    request: ScanRunRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """Ejecutar un scan para un asset.

    Args:
        request: Payload con asset y perfil.
        db: Sesion activa de SQLAlchemy.
        current_user: Usuario autenticado.

    Returns:
        Resultado devuelto por el servicio de scans.
    """
    try:
        return run_scan(
            db=db,
            asset_id=request.asset_id,
            profile=request.profile,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/{scan_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_scan(
    scan_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> None:
    """Eliminar un scan existente.

    Args:
        scan_id: Identificador unico del scan.
        db: Sesion activa de SQLAlchemy.
        current_user: Usuario autenticado.
    """
    db_scan = get_scan(db, scan_id)

    if not db_scan:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Escaneo no encontrado",
        )

    delete_scan(
        db,
        db_scan,
    )
