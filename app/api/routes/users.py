from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_active_user
from app.database.deps import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import (
    create_user,
    get_user_by_email,
    get_user_by_username,
    get_users,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/",
    response_model=list[UserResponse],
)
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    return get_users(db)


@router.post(
    "/",
    response_model=UserResponse,
)
def create_new_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    if get_user_by_username(db, user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario ya existe",
        )

    if get_user_by_email(db, user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya existe",
        )

    return create_user(db, user)
