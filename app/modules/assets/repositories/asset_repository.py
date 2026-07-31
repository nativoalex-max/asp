"""Repositorio encargado del acceso a datos de los Assets."""

from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.assets.model import Asset


def get_assets(db: Session):
    """Obtener todos los Assets ordenados por nombre."""
    return db.query(Asset).order_by(Asset.name).all()


def get_asset_by_id(db: Session, asset_id: UUID):
    """Obtener un Asset por su identificador."""
    return db.query(Asset).filter(Asset.id == asset_id).first()


def get_asset_by_ip(db: Session, ip_address: str):
    """Obtener un Asset por su dirección IP."""
    return db.query(Asset).filter(Asset.ip_address == ip_address).first()
