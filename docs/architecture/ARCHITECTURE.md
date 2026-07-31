# Arquitectura Base del Proyecto ASP

## Objetivo

Definir una arquitectura estándar para todos los módulos del proyecto ASP con el fin de garantizar mantenibilidad, escalabilidad, reutilización y facilidad de pruebas.

---

# Principios

Cada módulo debe cumplir los siguientes principios:

- Responsabilidad única.
- Bajo acoplamiento.
- Alta cohesión.
- Reutilización.
- Código fácilmente testeable.
- Compatibilidad con FastAPI y SQLAlchemy.

---

# Estructura estándar

Cada módulo deberá tener la siguiente estructura:

app/modules/<modulo>/

    model.py

    schema.py

    routes.py

    services/

        crud_service.py

    repositories/

        repository.py

    validators/

        validator.py

---

# Responsabilidad de cada capa

## Routes

Responsable de:

- recibir solicitudes HTTP
- validar autenticación
- invocar el Service
- devolver respuestas HTTP

No debe contener lógica de negocio.

---

## Services

Responsable de:

- reglas de negocio
- coordinación entre componentes
- orquestación del flujo

No debe realizar consultas SQL directamente.

---

## Repository

Responsable únicamente del acceso a datos.

Debe contener:

- consultas
- inserciones
- actualizaciones
- eliminaciones

No debe contener reglas de negocio.

---

## Validators

Responsable de validar:

- reglas funcionales
- integridad
- consistencia

Debe lanzar excepciones controladas cuando una regla no se cumpla.

---

## Schema

Define los contratos de entrada y salida.

No contiene lógica.

---

## Model

Representa las entidades SQLAlchemy.

---

# Flujo estándar

HTTP Request

↓

Route

↓

Service

↓

Validator

↓

Repository

↓

SQLAlchemy

↓

PostgreSQL

---

# Reglas

Nunca:

- SQL en Routes.
- SQL en Validators.
- HTTPException en Repository.
- lógica de negocio en Routes.

Siempre:

- Validar antes de persistir.
- Mantener compatibilidad hacia atrás.
- Documentar cambios importantes.

---

# Convenciones

## Archivos

crud_service.py

drawer_service.py

repository.py

validator.py

---

## Métodos Repository

get_by_id()

list()

save()

delete()

---

## Métodos Service

create()

update()

remove()

get()

list()

---

# Objetivos futuros

La arquitectura debe soportar sin modificaciones importantes:

- Discovery
- Scans
- Vulnerabilidades
- Dashboard
- Reportes
- API REST
- Automatización
- Integraciones

---

# Beneficios

- Código mantenible.
- Refactorizaciones simples.
- Fácil incorporación de nuevos desarrolladores.
- Módulos consistentes.
- Mayor facilidad para pruebas unitarias.
---

# Estructura de un módulo

Ejemplo:

app/modules/assets/

```
model.py
schema.py
routes.py

services/
    crud_service.py
    drawer_service.py

repositories/
    asset_repository.py

validators/
    asset_validator.py

__init__.py
```

---

# Flujo de ejecución

```
Cliente

↓

FastAPI Route

↓

Service

↓

Validator

↓

Repository

↓

SQLAlchemy

↓

PostgreSQL

↓

Service

↓

Route

↓

Respuesta JSON
```

---

# Principios de desarrollo

Cada nueva funcionalidad deberá cumplir las siguientes reglas:

1. Todo desarrollo inicia con un Documento de Diseño Técnico (TDD).
2. Ningún cambio mayor se implementa sin revisión de arquitectura.
3. Los Services no realizan consultas SQL.
4. Los Repository no contienen reglas de negocio.
5. Los Validators no realizan acceso a base de datos directamente.
6. Las Routes únicamente gestionan HTTP.
7. Cada historia de usuario debe mantener compatibilidad hacia atrás cuando sea posible.
8. Todo cambio debe pasar por revisión de Diff antes de ser aceptado.
