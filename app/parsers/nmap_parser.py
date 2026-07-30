import xml.etree.ElementTree as ET


class NmapParser:

    @staticmethod
    def parse(xml_file: str):

        tree = ET.parse(xml_file)
        root = tree.getroot()

        hosts = []

        for host in root.findall("host"):

            address = host.find("address")

            ip = address.attrib.get("addr")

            host_data = {
                "ip": ip,
                "ports": [],
                "hostnames": [],
                "os": None,
            }

            hostnames = host.find("hostnames")

            if hostnames is not None:

                for hostname in hostnames.findall("hostname"):

                    host_data["hostnames"].append(
                        hostname.attrib.get("name")
                    )

            os = host.find("os")

            if os is not None:

                osmatch = os.find("osmatch")

                if osmatch is not None:

                    host_data["os"] = osmatch.attrib.get("name")

            ports = host.find("ports")

            if ports is None:
                hosts.append(host_data)
                continue

            for port in ports.findall("port"):

                state = port.find("state")
                service = port.find("service")

                host_data["ports"].append(
                    {
                        "port": int(port.attrib["portid"]),
                        "protocol": port.attrib["protocol"],
                        "state": state.attrib.get("state"),
                        "service": (
                            service.attrib.get("name")
                            if service is not None else None
                        ),
                        "product": (
                            service.attrib.get("product")
                            if service is not None else None
                        ),
                        "version": (
                            service.attrib.get("version")
                            if service is not None else None
                        ),
                        "extra_info": (
                            service.attrib.get("extrainfo")
                            if service is not None else None
                        ),
                        "cpe": (
                            service.findtext("cpe")
                            if service is not None else None
                        ),
                    }
                )

            hosts.append(host_data)

        return hosts
