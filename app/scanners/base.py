from abc import ABC, abstractmethod


class BaseScanner(ABC):
    """
    Clase base para todos los escáneres de ASP.
    """

    @abstractmethod
    def scan(self, target: str):
        """
        Ejecuta un escaneo sobre el objetivo indicado.
        """
        raise NotImplementedError
