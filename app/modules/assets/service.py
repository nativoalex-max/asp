from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.assets.model import Asset
from app.modules.assets.schema import AssetCreate, AssetUpdate


def get_assets(db: Session):
    return db.query(Asset).order_by(Asset.name).all()


def get_asset_by_id(db: Session, asset_id: UUID):
    return db.query(Asset).filter(Asset.id == asset_id).first()


def get_asset_by_ip(db: Session, ip_address: str):
    return db.query(Asset).filter(Asset.ip_address == ip_address).first()


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


def update_asset(
    db: Session,
    db_asset: Asset,
    asset: AssetUpdate,
):
    data = asset.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(db_asset, key, value)

    db.commit()
    db.refresh(db_asset)

    return db_asset


def delete_asset(
    db: Session,
    db_asset: Asset,
):
    db.delete(db_asset)
    db.commit()
