"""Schemas de entrada y salida para el modulo Scans."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ScanRunRequest(BaseModel):
    """Payload para ejecutar un scan."""

    asset_id: UUID
    profile: str = "quick"


class ScanResponse(BaseModel):
    """Respuesta basica de un scan."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    asset_id: UUID
    scanner: str
    target: str
    profile: str
    status: str
    started_at: datetime
    finished_at: datetime | None
    duration: int | None


class ScanPortResponse(BaseModel):
    """Respuesta de puerto descubierto en un scan."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    port: int
    protocol: str
    state: str
    service: str | None
    product: str | None
    version: str | None
    extra_info: str | None


class ScanDetailResponse(ScanResponse):
    """Respuesta detallada de scan con puertos."""

    ports: list[ScanPortResponse] = []
