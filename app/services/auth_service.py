from sqlalchemy.orm import Session

from app.core.security import create_access_token, verify_password
from app.models.user import User
from app.services.user_service import get_user_by_username


def authenticate_user(
    db: Session,
    username: str,
    password: str,
) -> User | None:
    user = get_user_by_username(db, username)

    if not user:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


def login(
    db: Session,
    username: str,
    password: str,
):
    user = authenticate_user(
        db,
        username,
        password,
    )

    if user is None:
        return None

    access_token = create_access_token(
        {
            "sub": user.username,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
