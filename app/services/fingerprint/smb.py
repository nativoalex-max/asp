from pathlib import Path
import subprocess


def smb_os_discovery(ip: str):

    command = [
        "sudo",
        "/usr/bin/nmap",
        "-Pn",
        "-p445",
        "--script",
        "smb-os-discovery",
        ip,
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )

    return result.stdout
