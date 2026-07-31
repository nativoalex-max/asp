"""Validador para verificar reglas de negocio relacionadas con los Assets."""

from sqlalchemy.orm import Session

from app.modules.assets.model import Asset
from app.modules.assets.schema import AssetCreate, AssetUpdate


def validate_create_asset(db: Session, asset: AssetCreate) -> None:
    """Punto de extension para validaciones previas a la creacion de assets.

    Args:
        db: Sesion activa de SQLAlchemy.
        asset: Datos de entrada del asset a crear.
    """


def validate_update_asset(db: Session, db_asset: Asset, asset: AssetUpdate) -> None:
    """Punto de extension para validaciones previas a la actualizacion de assets.

    Args:
        db: Sesion activa de SQLAlchemy.
        db_asset: Instancia persistida del asset a actualizar.
        asset: Datos de actualizacion del asset.
    """


def validate_delete_asset(db: Session, db_asset: Asset) -> None:
    """Punto de extension para validaciones previas a la eliminacion de assets.

    Args:
        db: Sesion activa de SQLAlchemy.
        db_asset: Instancia persistida del asset a eliminar.
    """
