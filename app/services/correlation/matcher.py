from sqlalchemy import or_, select

from app.database.session import SessionLocal
from app.modules.vulnerability_catalog.model import VulnerabilityCatalog


class CorrelationMatcher:

    @staticmethod
    def _normalize_cpe(cpe: str) -> str:
        """
        Convierte un CPE legacy (cpe:/o:microsoft:windows)
        a un prefijo compatible con CPE 2.3.

        cpe:/o:microsoft:windows
            ↓
        cpe:2.3:o:microsoft:windows
        """

        if not cpe:
            return ""

        if cpe.startswith("cpe:/"):
            return cpe.replace("cpe:/", "cpe:2.3:", 1)

        return cpe

    @staticmethod
    def find_by_cpe(cpe: str):

        if not cpe:
            return []

        db = SessionLocal()

        try:

            normalized = CorrelationMatcher._normalize_cpe(cpe)

            result = db.execute(
                select(VulnerabilityCatalog).where(
                    or_(
                        VulnerabilityCatalog.cpe.like(f"{normalized}%"),
                        VulnerabilityCatalog.cpe.like(f"{cpe}%"),
                    )
                )
            )

            vulnerabilities = result.scalars().all()

            # eliminar duplicados por CVE
            unique = {}

            for vuln in vulnerabilities:
                unique[vuln.cve] = vuln

            return list(unique.values())

        finally:
            db.close()
