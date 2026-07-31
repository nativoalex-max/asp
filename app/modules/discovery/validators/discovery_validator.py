"""Validador para verificar reglas de negocio relacionadas con Discovery."""


def validate_run_discovery(db, client_id, target: str, profile: str = "quick") -> None:
    """Punto de extension para validaciones previas a la ejecucion de discovery.

    Args:
        db: Sesion activa de SQLAlchemy.
        client_id: Identificador del cliente para el discovery.
        target: Objetivo del descubrimiento.
        profile: Perfil de escaneo a ejecutar.
    """


def validate_discovered_host(host) -> None:
    """Punto de extension para validaciones por host descubierto.

    Args:
        host: Host descubierto por el escaneo.
    """


def validate_before_scan(db, asset_id, profile: str = "quick") -> None:
    """Punto de extension para validaciones previas a ejecutar un scan.

    Args:
        db: Sesion activa de SQLAlchemy.
        asset_id: Identificador del asset a escanear.
        profile: Perfil de escaneo a ejecutar.
    """