from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class VulnerabilityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID

    scan_port_id: UUID

    cve: str

    cvss: Decimal | None = None

    severity: str | None = None

    description: str | None = None

    reference: str | None = None

    source: str

    published_at: datetime | None = None

    created_at: datetime
