from sqlalchemy import select

from app.database.session import SessionLocal
from app.modules.vulnerabilities.model import Vulnerability


class VulnerabilityService:

    def list(
        self,
        skip: int = 0,
        limit: int = 100,
    ):

        session = SessionLocal()

        try:

            stmt = (
                select(Vulnerability)
                .offset(skip)
                .limit(limit)
            )

            return session.scalars(stmt).all()

        finally:

            session.close()

    def get_by_cve(
        self,
        cve: str,
    ):

        session = SessionLocal()

        try:

            stmt = (
                select(Vulnerability)
                .where(
                    Vulnerability.cve == cve
                )
            )

            return session.scalars(stmt).all()

        finally:

            session.close()
