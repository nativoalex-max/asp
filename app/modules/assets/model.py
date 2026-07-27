import uuid

from sqlalchemy import Boolean, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("clients.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    hostname: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    ip_address: Mapped[str] = mapped_column(
        String(45),
        nullable=False,
    )

    dns_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    mac_address: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    operating_system: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    os_version: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    manufacturer: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    model: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    asset_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    environment: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    criticality: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    owner: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    location: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )
