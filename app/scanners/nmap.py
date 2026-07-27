import subprocess
from pathlib import Path

from app.scanners.base import BaseScanner


class NmapScanner(BaseScanner):
    """
    Implementación del escáner Nmap para ASP.
    """

    OUTPUT_DIR = Path("/tmp/asp_scans")

    def __init__(self):
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    def scan(self, target: str):
        return self.quick_scan(target)

    def quick_scan(self, target: str):
        """
        Ejecuta un escaneo rápido (-T4 -F)
        y guarda la salida en XML.
        """

        xml_file = self.OUTPUT_DIR / f"{target.replace('/', '_')}.xml"

        command = [
            "nmap",
            "-T4",
            "-F",
            "-oX",
            str(xml_file),
            target,
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        return {
            "success": result.returncode == 0,
            "target": target,
            "xml_file": str(xml_file),
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
