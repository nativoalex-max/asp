import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base

if TYPE_CHECKING:
    from app.modules.assets.model import Asset
    from app.modules.scans.port_model import ScanPort


class Scan(Base):
    __tablename__ = "scans"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    asset_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("assets.id"),
        nullable=False,
    )

    scanner: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="nmap",
    )

    target: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    profile: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="quick",
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="pending",
    )

    command: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    xml_file: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    duration: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    asset: Mapped["Asset"] = relationship(
        "Asset",
        back_populates="scans",
    )

    ports: Mapped[list["ScanPort"]] = relationship(
        "ScanPort",
        back_populates="scan",
        cascade="all, delete-orphan",
    )
