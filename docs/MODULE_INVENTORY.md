# Inventario técnico de módulos de ASP

Este documento recoge el inventario verificado de los módulos presentes en la carpeta app/modules, con base en los archivos y referencias del proyecto existentes en el estado actual.

## Resumen general

| Módulo | Estado | Observación general |
|---|---|---|
| Assets | Parcial | Existen modelo, schema, rutas y un servicio inicial para el drawer, pero hay referencias a operaciones CRUD que no se observan implementadas en el servicio actual. |
| Clients | Parcial | Existen modelo, schema, rutas y servicio con operaciones CRUD básicas. |
| Dashboard | Parcial | Existen router, servicio de estadísticas y vista web asociada. |
| Discovery | Parcial | Existen modelo, rutas, servicio y job service, pero no hay schema dedicado y las rutas son limitadas a la ejecución del flujo. |
| Scans | Parcial | Existen modelo, rutas, schema y servicio para ejecutar y consultar scans. |
| Vulnerabilities | Parcial | Existen modelo, schema, router y servicio con operaciones de lectura. |
| Vulnerability Catalog | Parcial | Existen modelo, schema, router y servicio con operaciones de lectura. |

---

## 1. Assets

- Estado: Parcial
- Modelos:
  - Asset en [app/modules/assets/model.py](../app/modules/assets/model.py)
- Schemas:
  - AssetBase
  - AssetCreate
  - AssetUpdate
  - AssetResponse
  - Archivo: [app/modules/assets/schema.py](../app/modules/assets/schema.py)
- Services:
  - get_asset_drawer en [app/modules/assets/service.py](../app/modules/assets/service.py)
  - No se encontraron implementaciones de create_asset, get_assets, get_asset_by_id, get_asset_by_ip, update_asset o delete_asset en el servicio actual, aunque las rutas las importan.
- Routers:
  - [app/modules/assets/routes.py](../app/modules/assets/routes.py)
  - Endpoints existentes: GET /assets/, GET /assets/{asset_id}, GET /assets/view/{asset_id}, POST /assets/, PUT /assets/{asset_id}, DELETE /assets/{asset_id}
- Templates:
  - [app/templates/assets/index.html](../app/templates/assets/index.html)
- JavaScript:
  - [app/static/js/assets.js](../app/static/js/assets.js)
- CSS:
  - [app/static/css/assets.css](../app/static/css/assets.css)
- Dependencias:
  - Depende de [app/modules/clients/service.py](../app/modules/clients/service.py) para validar el cliente asociado.
  - Depende de los modelos de scans y vulnerabilidades para construir la información del drawer.
  - Se integra desde [app/api/routes/dashboard.py](../app/api/routes/dashboard.py) para las páginas web.
- Funcionalidades implementadas:
  - Gestión básica de activos a nivel de rutas.
  - Servicio inicial para construir un payload enriquecido del drawer.
  - Vista web con panel de drawer y listado de activos.
- Funcionalidades faltantes o pendientes de verificación:
  - No se encontró una implementación de servicio completa para las operaciones CRUD importadas por las rutas.
  - La lógica del drawer no está conectada a una respuesta de API completamente consolidada en la UI actual.

---

## 2. Clients

- Estado: Parcial
- Modelos:
  - Client en [app/modules/clients/model.py](../app/modules/clients/model.py)
- Schemas:
  - ClientBase
  - ClientCreate
  - ClientUpdate
  - ClientResponse
  - Archivo: [app/modules/clients/schema.py](../app/modules/clients/schema.py)
- Services:
  - get_clients
  - get_client_by_id
  - get_client_by_code
  - create_client
  - update_client
  - delete_client
  - Archivo: [app/modules/clients/service.py](../app/modules/clients/service.py)
- Routers:
  - [app/modules/clients/routes.py](../app/modules/clients/routes.py)
  - Endpoints existentes: GET /clients/, GET /clients/{client_id}, POST /clients/, PUT /clients/{client_id}, DELETE /clients/{client_id}
- Templates:
  - No se encontró una plantilla específica para clientes.
- JavaScript:
  - No se encontró JavaScript específico para clientes.
- Dependencias:
  - Depende de [app/api/dependencies.py](../app/api/dependencies.py) para la protección de rutas por usuario autenticado.
  - No se observaron dependencias directas con otros módulos de app/modules.
- Funcionalidades implementadas:
  - CRUD completo a nivel de rutas y servicio.
  - Validaciones de unicidad por código.
- Funcionalidades faltantes o pendientes de verificación:
  - No se encontró una interfaz web dedicada para clientes.

---

## 3. Dashboard

- Estado: Parcial
- Modelos:
  - No se encontró un modelo propio del módulo.
- Schemas:
  - No se encontró un schema propio del módulo.
- Services:
  - DashboardService con get_statistics en [app/modules/dashboard/service.py](../app/modules/dashboard/service.py)
- Routers:
  - [app/modules/dashboard/routes.py](../app/modules/dashboard/routes.py)
  - Endpoint existente: GET /api/dashboard/summary
- Templates:
  - [app/templates/dashboard/index.html](../app/templates/dashboard/index.html)
- JavaScript:
  - [app/static/js/dashboard.js](../app/static/js/dashboard.js)
- CSS:
  - [app/static/css/dashboard.css](../app/static/css/dashboard.css)
- Dependencias:
  - Reúne métricas de Asset, Scan, ScanPort y Vulnerability.
  - Se integra desde [app/api/router.py](../app/api/router.py) como router de API.
- Funcionalidades implementadas:
  - Resumen de plataforma con conteos de assets, scans, puertos, vulnerabilidades y riesgo estimado.
- Funcionalidades faltantes o pendientes de verificación:
  - No se encontró evidencia de más endpoints del dashboard más allá del resumen actual.

---

## 4. Discovery

- Estado: Parcial
- Modelos:
  - DiscoveryJob en [app/modules/discovery/model.py](../app/modules/discovery/model.py)
- Schemas:
  - No se encontró un schema dedicado; el archivo [app/modules/discovery/schema.py](../app/modules/discovery/schema.py) existe vacío.
- Services:
  - run_discovery en [app/modules/discovery/service.py](../app/modules/discovery/service.py)
  - Job service con create_job, update_progress, finish_job y fail_job en [app/modules/discovery/job_service.py](../app/modules/discovery/job_service.py)
- Routers:
  - [app/modules/discovery/routes.py](../app/modules/discovery/routes.py)
  - Endpoints existentes: GET /discovery/, GET /discovery/new, POST /discovery/start
- Templates:
  - [app/templates/discovery/index.html](../app/templates/discovery/index.html)
  - [app/templates/discovery/create.html](../app/templates/discovery/create.html)
  - [app/templates/discovery/result.html](../app/templates/discovery/result.html)
- JavaScript:
  - No se encontró JavaScript específico para discovery.
- Dependencias:
  - Usa [app/modules/assets/schema.py](../app/modules/assets/schema.py) y [app/modules/assets/service.py](../app/modules/assets/service.py) para crear activos a partir del descubrimiento.
  - Usa [app/modules/scans/service.py](../app/modules/scans/service.py) para ejecutar scans por cada host encontrado.
  - Usa parsers y scanners externos de la aplicación.
- Funcionalidades implementadas:
  - Flujo de descubrimiento de hosts con creación automática de activos y ejecución de scans.
  - Seguimiento de progreso de trabajo en el modelo DiscoveryJob.
- Funcionalidades faltantes o pendientes de verificación:
  - No se encontró un schema de entrada/salida dedicado para el módulo.
  - No se encontraron endpoints para listar, consultar o modificar jobs de discovery aparte del flujo inicial.

---

## 5. Scans

- Estado: Parcial
- Modelos:
  - Scan en [app/modules/scans/model.py](../app/modules/scans/model.py)
  - ScanPort en [app/modules/scans/port_model.py](../app/modules/scans/port_model.py)
- Schemas:
  - ScanRunRequest
  - ScanResponse
  - ScanPortResponse
  - ScanDetailResponse
  - Archivo: [app/modules/scans/schema.py](../app/modules/scans/schema.py)
- Services:
  - get_scan
  - list_scans
  - delete_scan
  - run_scan
  - Archivo: [app/modules/scans/service.py](../app/modules/scans/service.py)
- Routers:
  - [app/modules/scans/routes.py](../app/modules/scans/routes.py)
  - Endpoints existentes: GET /scans/, GET /scans/{scan_id}, POST /scans/run, DELETE /scans/{scan_id}
- Templates:
  - No se encontró una plantilla específica para scans.
- JavaScript:
  - No se encontró JavaScript específico para scans.
- Dependencias:
  - Usa [app/modules/assets/service.py](../app/modules/assets/service.py) para validar el activo asociado.
  - Usa la lógica de fingerprint y correlación para generar vulnerabilidades a partir de los resultados del scan.
  - Se integra con los modelos de vulnerabilidades y scan ports.
- Funcionalidades implementadas:
  - Ejecución de scans con scanner Nmap y parsing de resultados.
  - Registro de puertos, fingerprints y vulnerabilidades asociadas.
  - Endpoints de listado, detalle y eliminación.
- Funcionalidades faltantes o pendientes de verificación:
  - No se encontraron plantillas ni UI específica para el módulo.

---

## 6. Vulnerabilities

- Estado: Parcial
- Modelos:
  - Vulnerability en [app/modules/vulnerabilities/model.py](../app/modules/vulnerabilities/model.py)
- Schemas:
  - VulnerabilityResponse en [app/modules/vulnerabilities/schema.py](../app/modules/vulnerabilities/schema.py)
- Services:
  - VulnerabilityService con list y get_by_cve en [app/modules/vulnerabilities/service.py](../app/modules/vulnerabilities/service.py)
- Routers:
  - [app/modules/vulnerabilities/router.py](../app/modules/vulnerabilities/router.py)
  - Endpoints existentes: GET /api/vulnerabilities/, GET /api/vulnerabilities/cve/{cve}
- Templates:
  - No se encontró una plantilla específica para vulnerabilidades.
- JavaScript:
  - No se encontró JavaScript específico para vulnerabilidades.
- Dependencias:
  - Usa el modelo de Vulnerability y el servicio de sesión de base de datos.
  - Se relaciona con ScanPort a través del modelo.
- Funcionalidades implementadas:
  - Consulta de vulnerabilidades por listado y por CVE.
- Funcionalidades faltantes o pendientes de verificación:
  - No se encontraron endpoints de escritura ni UI asociada.

---

## 7. Vulnerability Catalog

- Estado: Parcial
- Modelos:
  - VulnerabilityCatalog en [app/modules/vulnerability_catalog/model.py](../app/modules/vulnerability_catalog/model.py)
- Schemas:
  - VulnerabilityCatalogResponse en [app/modules/vulnerability_catalog/schema.py](../app/modules/vulnerability_catalog/schema.py)
- Services:
  - VulnerabilityCatalogService con list y get_by_cve en [app/modules/vulnerability_catalog/service.py](../app/modules/vulnerability_catalog/service.py)
- Routers:
  - [app/modules/vulnerability_catalog/router.py](../app/modules/vulnerability_catalog/router.py)
  - Endpoints existentes: GET /api/vulnerability-catalog/, GET /api/vulnerability-catalog/{cve}
- Templates:
  - No se encontró una plantilla específica para el catálogo.
- JavaScript:
  - No se encontró JavaScript específico para el catálogo.
- Dependencias:
  - Usa el modelo de VulnerabilityCatalog y el servicio de sesión de base de datos.
  - Se usa desde la correlación de vulnerabilidades en servicios transversales del proyecto.
- Funcionalidades implementadas:
  - Consulta de catálogo por listado y por CVE.
- Funcionalidades faltantes o pendientes de verificación:
  - No se encontraron endpoints de escritura ni UI asociada.

---

## Observaciones generales

- La arquitectura del proyecto está organizada por módulos con separación clara entre modelo, schema, servicio y router.
- El módulo Assets es el que muestra la mayor mezcla entre lógica de UI, rutas y servicios, y por ello es el punto donde más conviene revisar la coherencia entre backend y frontend.
- En varios módulos, las rutas existen y los servicios están presentes, pero la capa de interfaz web no está desarrollada de forma completa.
- En algunos casos, como Assets y Discovery, hay referencias a funciones o contratos de servicio que no se observan implementados en el archivo de servicio revisado, por lo que conviene verificar esas dependencias antes de introducir cambios.
