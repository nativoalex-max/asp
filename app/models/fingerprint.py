import uuid

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class Fingerprint(Base):
    __tablename__ = "fingerprints"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    scan_port_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("scan_ports.id", ondelete="CASCADE"),
        nullable=False,
    )

    source: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    vendor: Mapped[str | None] = mapped_column(
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

    cpe: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    confidence: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    scan_port: Mapped["ScanPort"] = relationship(
        "ScanPort",
        back_populates="fingerprints",
    )
