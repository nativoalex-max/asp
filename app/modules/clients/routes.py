from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user
from app.database.deps import get_db
from app.models.user import User

from app.modules.clients.schema import (
    ClientCreate,
    ClientResponse,
    ClientUpdate,
)
from app.modules.clients.service import (
    create_client,
    delete_client,
    get_client_by_code,
    get_client_by_id,
    get_clients,
    update_client,
)

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
)


@router.get(
    "/",
    response_model=list[ClientResponse],
)
def list_clients(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return get_clients(db)


@router.get(
    "/{client_id}",
    response_model=ClientResponse,
)
def get_client(
    client_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    client = get_client_by_id(db, client_id)

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado",
        )

    return client


@router.post(
    "/",
    response_model=ClientResponse,
    status_code=status.HTTP_201_CREATED,
)
def new_client(
    client: ClientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    if get_client_by_code(db, client.code):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El código del cliente ya existe",
        )

    return create_client(db, client)


@router.put(
    "/{client_id}",
    response_model=ClientResponse,
)
def edit_client(
    client_id: UUID,
    client: ClientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_client = get_client_by_id(db, client_id)

    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado",
        )

    if client.code:
        existing = get_client_by_code(db, client.code)

        if existing and existing.id != db_client.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El código del cliente ya existe",
            )

    return update_client(
        db,
        db_client,
        client,
    )


@router.delete(
    "/{client_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_client(
    client_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    db_client = get_client_by_id(db, client_id)

    if not db_client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente no encontrado",
        )

    delete_client(
        db,
        db_client,
    )

    return
