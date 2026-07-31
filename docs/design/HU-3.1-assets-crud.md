# HU-3.1 – CRUD Completo de Assets

## Estado
📋 En diseño

---

# Objetivo

Completar el módulo Assets para que disponga de un CRUD completo, mantenible y alineado con la arquitectura del proyecto ASP.

---

# Problema actual

El módulo Assets actualmente implementa las operaciones principales de CRUD y el Asset Drawer, pero concentra responsabilidades en el archivo `service.py`.

Esto dificulta la evolución del módulo y aumenta el riesgo de introducir errores cuando se agregan nuevas funcionalidades.

---

# Objetivos del Sprint

- Mantener compatibilidad con la API existente.
- Reducir el tamaño y responsabilidad de `service.py`.
- Separar acceso a datos de la lógica de negocio.
- Centralizar las validaciones.
- Preparar el módulo para futuras funcionalidades.
- Mantener el Drawer funcionando sin modificaciones funcionales.

---

# Arquitectura actual

```
Routes
    │
    ▼
Service
    │
    ▼
SQLAlchemy
```

---

# Arquitectura objetivo

```
Routes
    │
    ▼
AssetService
    │
 ┌──┴──────────────┐
 ▼                 ▼
Repository     Validators
 │
 ▼
SQLAlchemy
```

---

# Archivos actuales

- model.py
- schema.py
- routes.py
- service.py

---

# Archivos nuevos propuestos

- repository.py
- validators.py

---

# Archivos que serán modificados

- routes.py
- service.py

---

# Responsabilidad de cada archivo

## routes.py

Responsable únicamente de recibir solicitudes HTTP y delegar el trabajo al servicio.

No debe contener reglas de negocio.

---

## service.py

Responsable únicamente de la lógica de negocio.

No debe realizar consultas SQL directamente.

---

## repository.py

Responsable del acceso a la base de datos.

Contendrá exclusivamente operaciones sobre SQLAlchemy.

---

## validators.py

Responsable de todas las validaciones funcionales del módulo.

Ejemplos:

- IP duplicada.
- Cliente inexistente.
- Activo inexistente.
- Validaciones futuras.

---

# Casos de uso

- Listar activos.
- Consultar un activo.
- Crear un activo.
- Actualizar un activo.
- Eliminar un activo.
- Consultar información del Drawer.

---

# Riesgos

- Romper compatibilidad con el Drawer.
- Duplicar lógica entre Repository y Service.
- Introducir validaciones repetidas.

---

# Estrategia de implementación

## Fase 1

Refactor interno.

No cambiar funcionalidad.

---

## Fase 2

Completar CRUD.

---

## Fase 3

Agregar búsqueda, filtros y paginación.

---

## Criterios de aceptación

- La API continúa funcionando.
- El Drawer mantiene su comportamiento.
- El Service disminuye su complejidad.
- Las consultas SQL quedan encapsuladas.
- Las validaciones quedan centralizadas.

---

# Definición de Done

- Arquitectura implementada.
- Código revisado.
- Pruebas funcionales aprobadas.
- Diff aprobado.
- Commit realizado.
- Push realizado.
---

# Dependencias

Este módulo depende de:

- Clients
- Authentication
- SQLAlchemy
- FastAPI
- Pydantic

---

# Pruebas requeridas

## API

- Crear activo.
- Editar activo.
- Eliminar activo.
- Consultar activo.
- Listar activos.

## Validaciones

- Cliente inexistente.
- IP duplicada.
- Activo inexistente.

## Frontend

- Crear desde formulario.
- Editar desde formulario.
- Eliminar desde la interfaz.
- Abrir Asset Drawer.
