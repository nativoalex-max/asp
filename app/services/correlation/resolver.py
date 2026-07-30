from app.services.correlation.matcher import CorrelationMatcher
from app.services.correlation.scorer import RiskScorer


class VulnerabilityResolver:

    @staticmethod
    def resolve(cpe: str):

        vulnerabilities = CorrelationMatcher.find_by_cpe(cpe)

        result = []

        for vuln in vulnerabilities:

            result.append(
                {
                    "cve": vuln.cve,
                    "severity": vuln.severity,
                    "cvss": float(vuln.cvss) if vuln.cvss else None,
                    "risk": RiskScorer.calculate(vuln.cvss),
                    "description": vuln.description,
                    "reference": vuln.reference,
                }
            )

        return result
