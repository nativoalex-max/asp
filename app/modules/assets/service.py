from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.assets.model import Asset
from app.modules.assets.repositories.asset_repository import (
    get_asset_by_id,
    get_asset_by_ip,
    get_assets,
)
from app.modules.assets.schema import AssetCreate, AssetUpdate
from app.modules.assets.services.drawer_service import (
    get_asset_drawer as get_asset_drawer_service,
)


def create_asset(db: Session, asset: AssetCreate):
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


def update_asset(db: Session, db_asset: Asset, asset: AssetUpdate):
    data = asset.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(db_asset, key, value)

    db.commit()
    db.refresh(db_asset)

    return db_asset


def delete_asset(db: Session, db_asset: Asset):
    db.delete(db_asset)
    db.commit()


def get_asset_drawer(db: Session, asset_id: UUID):
    return get_asset_drawer_service(db, asset_id)
