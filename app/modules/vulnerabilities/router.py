from fastapi import APIRouter

from app.modules.vulnerabilities.schema import (
    VulnerabilityResponse,
)
from app.modules.vulnerabilities.service import (
    VulnerabilityService,
)

router = APIRouter(
    prefix="/api/vulnerabilities",
    tags=["Vulnerabilities"],
)

service = VulnerabilityService()


@router.get(
    "/",
    response_model=list[VulnerabilityResponse],
)
def list_vulnerabilities(
    skip: int = 0,
    limit: int = 100,
):

    return service.list(skip, limit)


@router.get(
    "/cve/{cve}",
    response_model=list[VulnerabilityResponse],
)
def search_cve(
    cve: str,
):

    return service.get_by_cve(cve)
