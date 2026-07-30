import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.modules.scans.model import Scan
    from app.modules.vulnerabilities.model import Vulnerability
    from app.models.fingerprint import Fingerprint


class ScanPort(Base):
    __tablename__ = "scan_ports"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    scan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scans.id"),
        nullable=False,
    )

    port: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    protocol: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    state: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    service: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    product: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    version: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    extra_info: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    cpe: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    scan: Mapped["Scan"] = relationship(
        "Scan",
        back_populates="ports",
    )

    vulnerabilities: Mapped[list["Vulnerability"]] = relationship(
        "Vulnerability",
        back_populates="scan_port",
        cascade="all, delete-orphan",
    )

    fingerprints: Mapped[list["Fingerprint"]] = relationship(
        "Fingerprint",
        back_populates="scan_port",
        cascade="all, delete-orphan",
    )
