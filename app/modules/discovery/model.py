import uuid
from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class DiscoveryJob(Base):
    __tablename__ = "discovery_jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
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

    total_hosts: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    processed_hosts: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
    )

    current_host: Mapped[str | None] = mapped_column(
        String(255),
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
