"""Servicio tecnico para ejecutar Nmap y parsear hosts."""

from typing import Any

from app.parsers.nmap_parser import NmapParser
from app.scanners.nmap import NmapScanner


def execute_scan(
    target: str,
    profile: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    """Ejecutar escaneo Nmap y parsear hosts del XML.

    Args:
        target: Objetivo del escaneo.
        profile: Perfil de escaneo a ejecutar.

    Returns:
        Tupla con el resultado crudo del scanner y los hosts parseados.
    """
    scanner = NmapScanner()

    result = scanner.scan(
        target=target,
        profile=profile,
    )

    hosts = NmapParser.parse(result["xml_file"])

    return result, hosts
