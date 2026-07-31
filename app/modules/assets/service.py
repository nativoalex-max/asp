from uuid import UUID

from sqlalchemy.orm import Session

from app.modules.assets.model import Asset
from app.modules.assets.repositories.asset_repository import (
    get_asset_by_id as get_asset_by_id_repository,
    get_asset_by_ip as get_asset_by_ip_repository,
    get_assets as get_assets_repository,
)
from app.modules.assets.schema import AssetCreate, AssetUpdate
from app.modules.assets.services.crud_service import (
    create_asset as create_asset_service,
    delete_asset as delete_asset_service,
    update_asset as update_asset_service,
)
from app.modules.assets.services.drawer_service import (
    get_asset_drawer as get_asset_drawer_service,
)


def create_asset(db: Session, asset: AssetCreate):
    return create_asset_service(db, asset)


def update_asset(db: Session, db_asset: Asset, asset: AssetUpdate):
    return update_asset_service(db, db_asset, asset)


def delete_asset(db: Session, db_asset: Asset):
    return delete_asset_service(db, db_asset)


def get_assets(db: Session, skip: int = 0, limit: int = 100):
    return get_assets_repository(db, skip, limit)


def get_asset_by_id(db: Session, asset_id: UUID):
    return get_asset_by_id_repository(db, asset_id)


def get_asset_by_ip(db: Session, ip_address: str):
    return get_asset_by_ip_repository(db, ip_address)


def get_asset_drawer(db: Session, asset_id: UUID):
    return get_asset_drawer_service(db, asset_id)
