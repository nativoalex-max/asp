from app.parsers.nmap_parser import NmapParser
from app.scanners.nmap import NmapScanner


def execute_discovery_scan(
    target: str,
    profile: str,
):
    scanner = NmapScanner()

    result = scanner.scan(
        target=target,
        profile=profile,
    )

    if not result["success"]:
        raise Exception(result["stderr"])

    hosts = NmapParser.parse(result["xml_file"])

    return hosts