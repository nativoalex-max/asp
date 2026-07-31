from app.modules.scans.port_model import ScanPort


def create_scan_ports(db, scan, hosts):
    total_ports = 0
    created_ports = []

    for host in hosts:

        for port in host["ports"]:

            db_port = ScanPort(
                scan_id=scan.id,
                port=port["port"],
                protocol=port["protocol"],
                state=port["state"],
                service=port.get("service"),
                product=port.get("product"),
                version=port.get("version"),
                extra_info=port.get("extra_info"),
                cpe=port.get("cpe"),
            )

            db.add(db_port)
            created_ports.append(db_port)

            total_ports += 1

    db.flush()

    return created_ports, total_ports