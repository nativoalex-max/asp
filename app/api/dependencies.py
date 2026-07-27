from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import get_username_from_token, oauth2_scheme
from app.database.deps import get_db
from app.models.user import User
from app.services.user_service import get_user_by_username


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    username = get_username_from_token(token)

    user = get_user_by_username(
        db,
        username,
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo",
        )

    return current_user
