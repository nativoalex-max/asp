"""Repositorio encargado del acceso a datos de los Assets."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.assets.model import Asset


def get_assets(db: Session) -> list[Asset]:
    """Obtener todos los assets ordenados por nombre.

    Args:
        db: Sesion activa de SQLAlchemy.

    Returns:
        Lista de assets ordenada por nombre.
    """
    return db.query(Asset).order_by(Asset.name).all()


def get_asset_by_id(db: Session, asset_id: UUID) -> Asset | None:
    """Obtener un asset por su identificador.

    Args:
        db: Sesion activa de SQLAlchemy.
        asset_id: Identificador unico del asset.

    Returns:
        Instancia del asset si existe; en caso contrario, ``None``.
    """
    return db.query(Asset).filter(Asset.id == asset_id).first()


def get_asset_by_ip(db: Session, ip_address: str) -> Asset | None:
    """Obtener un asset por su direccion IP.

    Args:
        db: Sesion activa de SQLAlchemy.
        ip_address: Direccion IP del asset.

    Returns:
        Instancia del asset si existe; en caso contrario, ``None``.
    """
    return db.query(Asset).filter(Asset.ip_address == ip_address).first()
