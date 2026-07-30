import subprocess
from pathlib import Path

from app.scanners.base import BaseScanner


class NmapScanner(BaseScanner):

    OUTPUT_DIR = Path("/tmp/asp_scans")

    PROFILES = {
        "quick": [
            "-T4",
            "-F",
        ],
        "service": [
            "-sV",
            "--version-light",
            "-T4",
        ],
        "os": [
            "-O",
            "-T4",
        ],
        "aggressive": [
            "-A",
            "-T4",
        ],
        "full": [
            "-Pn",
            "-sS",
            "-sV",
            "--version-all",
            "-O",
            "-p-",
            "-T4",
        ],
    }

    def __init__(self):
        self.OUTPUT_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

    def scan(
        self,
        target: str,
        profile: str = "quick",
    ):

        options = self.PROFILES.get(
            profile,
            self.PROFILES["quick"],
        )

        xml_file = self.OUTPUT_DIR / f"{target.replace('/', '_')}.xml"

        command = [
            "sudo",
            "/usr/bin/nmap",
            *options,
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
            "profile": profile,
            "command": " ".join(command),
            "xml_file": str(xml_file),
            "stdout": result.stdout,
            "stderr": result.stderr,
        }
