from app.modules.assets.schema import AssetCreate
from app.modules.assets.service import create_asset, get_asset_by_ip


def get_or_create_asset(
    db,
    client_id,
    host,
    ip,
    created,
    existing,
):
    asset = get_asset_by_ip(db, ip)

    if asset is None:

        hostname = None

        if host["hostnames"]:
            hostname = host["hostnames"][0]

        asset = create_asset(
            db,
            AssetCreate(
                client_id=client_id,
                name=hostname or ip,
                hostname=hostname,
                ip_address=ip,
                dns_name=hostname,
                operating_system=host["os"],
                os_version=None,
                mac_address=None,
                manufacturer=None,
                model=None,
                asset_type="Host",
                environment=None,
                criticality=None,
                owner=None,
                location=None,
                description="Creado automáticamente por Discovery",
                is_active=True,
            ),
        )

        created += 1

    else:

        existing += 1

    return asset, created, existing