# ASP - Attack Surface Platform

## Project Overview

This is an enterprise Attack Surface Management Platform.

## Technology Stack

- Python 3.12
- FastAPI
- SQLAlchemy 2.x ORM
- PostgreSQL
- Alembic
- Bootstrap 5
- Vanilla JavaScript
- Jinja2

## Architecture Rules

Each module follows this structure:

- model.py
- schema.py
- service.py
- router.py

Business logic belongs in service.py.

Routers should remain thin.

Never move business logic into routers.

## Database Rules

Always use SQLAlchemy ORM.

Prefer:

- selectinload()
- joinedload() only when appropriate.

Never use raw SQL unless explicitly requested.

Primary keys are UUID.

Always preserve existing relationships.

## Coding Rules

Do not break existing CRUD.

Reuse existing services whenever possible.

Avoid duplicated code.

Write typed Python.

Follow PEP8.

Keep the same coding style used in the project.

## Frontend

Bootstrap 5 only.

Vanilla JavaScript.

No React.

No Angular.

No Vue.

## Development Philosophy

Always preserve backwards compatibility.

Generate complete implementations instead of placeholders.

Do not invent models or relationships.

Inspect the existing project before generating code.

If a model already exists, reuse it.

Never duplicate business logic.