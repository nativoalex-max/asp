from app.services.correlation.resolver import VulnerabilityResolver


class CorrelationEngine:

    @staticmethod
    def correlate(scan_ports):

        findings = []

        for port in scan_ports:

            if not port.cpe:
                continue

            vulns = VulnerabilityResolver.resolve(port.cpe)

            for vuln in vulns:

                vuln["scan_port"] = port

                findings.append(vuln)

        return findings
