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
                "ports": []
            }

            ports = host.find("ports")

            if ports is not None:

                for port in ports.findall("port"):

                    state = port.find("state")
                    service = port.find("service")

                    host_data["ports"].append(
                        {
                            "port": int(port.attrib["portid"]),
                            "protocol": port.attrib["protocol"],
                            "state": state.attrib["state"],
                            "service": (
                                service.attrib.get("name")
                                if service is not None
                                else None
                            ),
                        }
                    )

            hosts.append(host_data)

        return hosts
