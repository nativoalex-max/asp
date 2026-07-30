import json
from pathlib import Path


class NVDParser:
    """
    Carga el archivo JSON descargado desde el NVD y
    devuelve su contenido como un diccionario.
    """

    @staticmethod
    def load(file: Path) -> dict:

        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
