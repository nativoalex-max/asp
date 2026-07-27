import uuid

from pydantic import BaseModel, ConfigDict


class AssetBase(BaseModel):
    client_id: uuid.UUID
    name: str
    hostname: str | None = None
    ip_address: str
    dns_name: str | None = None
    mac_address: str | None = None
    operating_system: str | None = None
    os_version: str | None = None
    manufacturer: str | None = None
    model: str | None = None
    asset_type: str
    environment: str | None = None
    criticality: str | None = None
    owner: str | None = None
    location: str | None = None
    description: str | None = None
    is_active: bool = True


class AssetCreate(AssetBase):
    pass


class AssetUpdate(BaseModel):
    name: str | None = None
    hostname: str | None = None
    ip_address: str | None = None
    dns_name: str | None = None
    mac_address: str | None = None
    operating_system: str | None = None
    os_version: str | None = None
    manufacturer: str | None = None
    model: str | None = None
    asset_type: str | None = None
    environment: str | None = None
    criticality: str | None = None
    owner: str | None = None
    location: str | None = None
    description: str | None = None
    is_active: bool | None = None


class AssetResponse(AssetBase):
    id: uuid.UUID

    model_config = ConfigDict(
        from_attributes=True,
    )
