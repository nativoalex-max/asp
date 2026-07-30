from sqlalchemy import func
from sqlalchemy import select

from app.database.session import SessionLocal

from app.modules.assets.model import Asset
from app.modules.scans.model import Scan
from app.modules.scans.port_model import ScanPort
from app.modules.vulnerabilities.model import Vulnerability


class DashboardService:

    def get_statistics(self):

        session = SessionLocal()

        try:

            assets = session.scalar(
                select(func.count(Asset.id))
            ) or 0

            scans = session.scalar(
                select(func.count(Scan.id))
            ) or 0

            ports = session.scalar(
                select(func.count(ScanPort.id))
            ) or 0

            vulnerabilities = session.scalar(
                select(func.count(Vulnerability.id))
            ) or 0

            severity_rows = session.execute(
                select(
                    Vulnerability.severity,
                    func.count(Vulnerability.id)
                ).group_by(
                    Vulnerability.severity
                )
            ).all()

            severity = {
                "CRITICAL": 0,
                "HIGH": 0,
                "MEDIUM": 0,
                "LOW": 0,
                "INFO": 0,
                "UNKNOWN": 0,
            }

            for sev, qty in severity_rows:

                key = (sev or "UNKNOWN").upper()

                severity[key] = qty

            top_ports = session.execute(

                select(
                    ScanPort.port,
                    func.count(ScanPort.id)
                )
                .group_by(ScanPort.port)
                .order_by(func.count(ScanPort.id).desc())
                .limit(10)

            ).all()

            top_products = session.execute(

                select(
                    ScanPort.product,
                    func.count(ScanPort.id)
                )
                .where(
                    ScanPort.product.is_not(None)
                )
                .group_by(ScanPort.product)
                .order_by(func.count(ScanPort.id).desc())
                .limit(10)

            ).all()

            last_scan = session.scalar(

                select(Scan.started_at)
                .order_by(
                    Scan.started_at.desc()
                )
                .limit(1)

            )

            risk_score = (
                severity["CRITICAL"] * 10 +
                severity["HIGH"] * 7 +
                severity["MEDIUM"] * 4 +
                severity["LOW"] * 1
            )

            if risk_score > 100:
                risk_score = 100

            if risk_score >= 75:
                platform_status = "CRITICAL"

            elif risk_score >= 50:
                platform_status = "HIGH"

            elif risk_score >= 25:
                platform_status = "MEDIUM"

            else:
                platform_status = "LOW"

            return {

                "assets": assets,

                "scans": scans,

                "ports": ports,

                "vulnerabilities": vulnerabilities,

                "risk_score": risk_score,

                "platform_status": platform_status,

                "last_scan": (
                    last_scan.strftime("%Y-%m-%d %H:%M:%S")
                    if last_scan else None
                ),

                "severity": severity,

                "top_ports": [

                    {
                        "port": p,
                        "count": c
                    }

                    for p, c in top_ports

                ],

                "top_products": [

                    {
                        "product": p,
                        "count": c
                    }

                    for p, c in top_products

                ]

            }

        finally:

            session.close()
