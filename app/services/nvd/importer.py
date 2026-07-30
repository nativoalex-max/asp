from datetime import datetime
from decimal import Decimal

from sqlalchemy import select

from app.database.session import SessionLocal
from app.modules.vulnerability_catalog.model import VulnerabilityCatalog


class NVDImporter:

    @staticmethod
    def _parse_datetime(value):

        if not value:
            return None

        try:
            return datetime.fromisoformat(
                value.replace("Z", "+00:00")
            )
        except Exception:
            return None

    def import_data(self, data: dict):

        session = SessionLocal()

        try:

            vulnerabilities = data.get("vulnerabilities", [])

            total_new = 0
            total_updated = 0

            for item in vulnerabilities:

                cve = item.get("cve", {})

                cve_id = cve.get("id")

                if not cve_id:
                    continue

                existing = session.execute(
                    select(VulnerabilityCatalog).where(
                        VulnerabilityCatalog.cve == cve_id
                    )
                ).scalar_one_or_none()

                description = ""

                for d in cve.get("descriptions", []):

                    if d.get("lang") == "en":
                        description = d.get("value", "")
                        break

                severity = None
                cvss = None

                metrics = cve.get("metrics", {})

                if metrics.get("cvssMetricV31"):

                    metric = metrics["cvssMetricV31"][0]

                    severity = metric["cvssData"].get("baseSeverity")

                    cvss = Decimal(
                        str(metric["cvssData"].get("baseScore"))
                    )

                elif metrics.get("cvssMetricV30"):

                    metric = metrics["cvssMetricV30"][0]

                    severity = metric["cvssData"].get("baseSeverity")

                    cvss = Decimal(
                        str(metric["cvssData"].get("baseScore"))
                    )

                elif metrics.get("cvssMetricV2"):

                    metric = metrics["cvssMetricV2"][0]

                    severity = metric.get("baseSeverity")

                    cvss = Decimal(
                        str(metric["cvssData"].get("baseScore"))
                    )

                references = []

                for ref in cve.get("references", []):

                    url = ref.get("url")

                    if url:
                        references.append(url)

                reference = "\n".join(references)

                published = self._parse_datetime(
                    cve.get("published")
                )

                modified = self._parse_datetime(
                    cve.get("lastModified")
                )

                cpe = None
                vendor = None
                product = None
                version = None

                configurations = cve.get("configurations", [])

                for conf in configurations:

                    for node in conf.get("nodes", []):

                        for match in node.get("cpeMatch", []):

                            criteria = match.get("criteria")

                            if not criteria:
                                continue

                            cpe = criteria

                            parts = criteria.split(":")

                            if len(parts) >= 6:

                                vendor = parts[3]
                                product = parts[4]
                                version = parts[5]

                            break

                        if cpe:
                            break

                    if cpe:
                        break

                if existing:

                    existing.cpe = cpe
                    existing.vendor = vendor
                    existing.product = product
                    existing.version = version
                    existing.severity = severity
                    existing.cvss = cvss
                    existing.description = description
                    existing.reference = reference
                    existing.published_at = published
                    existing.modified_at = modified

                    total_updated += 1

                else:

                    session.add(

                        VulnerabilityCatalog(

                            cve=cve_id,
                            cpe=cpe,
                            vendor=vendor,
                            product=product,
                            version=version,
                            severity=severity,
                            cvss=cvss,
                            description=description,
                            reference=reference,
                            published_at=published,
                            modified_at=modified,

                        )

                    )

                    total_new += 1

            session.commit()

            print("=" * 70)
            print(f"Nuevos: {total_new}")
            print(f"Actualizados: {total_updated}")
            print("=" * 70)

        finally:

            session.close()
