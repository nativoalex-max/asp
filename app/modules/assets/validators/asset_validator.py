"""Validador para verificar reglas de negocio relacionadas con los Assets."""

from sqlalchemy.orm import Session

from app.modules.assets.model import Asset
from app.modules.assets.schema import AssetCreate, AssetUpdate


def validate_create_asset(db: Session, asset: AssetCreate):
    """Punto de extensión para validaciones previas a la creación de assets."""


def validate_update_asset(db: Session, db_asset: Asset, asset: AssetUpdate):
    """Punto de extensión para validaciones previas a la actualización de assets."""


def validate_delete_asset(db: Session, db_asset: Asset):
    """Punto de extensión para validaciones previas a la eliminación de assets."""
