"""Servicio de CRUD para orquestar operaciones básicas del módulo de Assets."""

from sqlalchemy.orm import Session

from app.modules.assets.model import Asset
from app.modules.assets.schema import AssetCreate, AssetUpdate
from app.modules.assets.validators.asset_validator import (
    validate_create_asset,
    validate_delete_asset,
    validate_update_asset,
)


def create_asset(db: Session, asset: AssetCreate) -> Asset:
    """Crear un asset y persistirlo en base de datos.

    Args:
        db: Sesion activa de SQLAlchemy.
        asset: Datos de entrada para crear el asset.

    Returns:
        Instancia del asset creada y refrescada desde base de datos.
    """
    validate_create_asset(db, asset)

    db_asset = Asset(
        client_id=asset.client_id,
        name=asset.name,
        hostname=asset.hostname,
        ip_address=asset.ip_address,
        dns_name=asset.dns_name,
        mac_address=asset.mac_address,
        operating_system=asset.operating_system,
        os_version=asset.os_version,
        manufacturer=asset.manufacturer,
        model=asset.model,
        asset_type=asset.asset_type,
        environment=asset.environment,
        criticality=asset.criticality,
        owner=asset.owner,
        location=asset.location,
        description=asset.description,
        is_active=asset.is_active,
    )

    db.add(db_asset)
    db.commit()
    db.refresh(db_asset)

    return db_asset


def update_asset(db: Session, db_asset: Asset, asset: AssetUpdate) -> Asset:
    """Actualizar un asset existente con campos parciales.

    Args:
        db: Sesion activa de SQLAlchemy.
        db_asset: Instancia persistida del asset a actualizar.
        asset: Datos de actualizacion parcial.

    Returns:
        Instancia del asset actualizada y refrescada.
    """
    validate_update_asset(db, db_asset, asset)

    data = asset.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(db_asset, key, value)

    db.commit()
    db.refresh(db_asset)

    return db_asset


def delete_asset(db: Session, db_asset: Asset) -> None:
    """Eliminar un asset existente.

    Args:
        db: Sesion activa de SQLAlchemy.
        db_asset: Instancia persistida del asset a eliminar.
    """
    validate_delete_asset(db, db_asset)

    db.delete(db_asset)
    db.commit()
