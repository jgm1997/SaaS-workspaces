# Arquitectura — Convenciones y flujos

## Convenciones de tablas

- PK: columna `pk` tipo UUID en todas las tablas.
  - Ejemplo: `pk UUID PRIMARY KEY DEFAULT gen_random_uuid()`
- Timestamps: `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`, `updated_at TIMESTAMPTZ`
- Soft delete: `deleted_at TIMESTAMPTZ` (NULL = activo)
- Nombres: snake_case para columnas y tablas (ej.: `workspace`, `project`, `user`, `rel1_rel2`)
- Índices: índices compuestos para consultas frecuentes (`workspace_pk`, `created_at`, etc.)

Ejemplo (Postgres):

```sql
CREATE TABLE workspace (
    pk UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL,
    slug TEXT UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ,
    deleted_at TIMESTAMPTZ
);
```

## Foreign keys

- Naming: `{child_table}_{ref_table}_pk` o `{ref_table}_pk`.
- Definición: `REFERENCES <table>(pk) ON DELETE CASCADE` o `RESTRICT` según el caso.
- Siempre indexar columnas FK para joins/queries.

Ejemplo:

```sql
CREATE TABLE projects (
    pk UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    workspace_pk UUID NOT NULL REFERENCES workspaces(pk) ON DELETE CASCADE,
    name TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
CREATE INDEX idx_projects_workspace_pk ON projects(workspace_pk);
```

## Multi-tenant (X-Workspace)

- Modelo recomendado: tenant-by-row (shared schema) + columna `workspace_pk` en entidades.
- Propagación del tenant: header HTTP `X-Workspace: <workspace-pk>` en cada request.
- Seguridad: middleware valida que el usuario pertenece al `workspace_pk` antes de ejecutar lógica.
- Alternativa: Row-Level Security (RLS) en DB para garantizar aislamiento por `current_setting` o session variable.

Recomendación:

- No confiar solo en el header: combinar token de usuario + verificación membership contra `workspace_pk`.

## Estructura de carpetas (sugerida)

- docs/
  - architecture.md
- src/
  - api/ (endpoints)
  - auth/ (login, refresh, middleware)
  - services/ (business logic)
  - db/ (migrations, seeds)
  - models/ (ORM / queries)
  - infra/ (deploy, terraform)
- tests/

## Flujo de autenticación

1. Usuario envía credenciales a `POST /auth/login` (o SSO).
2. Respuesta: `access_token` (JWT, corta vida) + `refresh_token`.
3. JWT incluye `sub=user_pk`, claims mínimos. No incluir workspace por defecto.
4. Cada request: Authorization header `Bearer <token>` + `X-Workspace: <workspace-pk>`.
5. Middleware:
   - Verifica JWT,
   - Verifica que `user_pk` está activo,
   - Verifica membership: `users_workspaces` contiene (user_pk, workspace_pk) y rol.
6. Refresh: `POST /auth/refresh` con refresh token → nuevo access token.
7. Logout/revocation: marcar refresh token como inválido en DB.

## Flujo de workspace

1. Crear workspace: `POST /workspaces` (owner = creador).
2. Tabla membership: `users_workspaces(pk, user_pk, workspace_pk, role, accepted_at, invited_by)`
3. Invitar:
   - Crear registro de invitación + token,
   - Enviar email con link,
   - Al aceptar: crear `users_workspaces` si no existe.
4. Roles: owner, admin, member (controlan permisos CRUD).
5. Eliminación: soft-delete del workspace; limpiar / transferir recursos según política.

## Flujo de projects

1. Crear proyecto: `POST /workspaces/:workspace_pk/projects` (verificar permisos).
2. `projects.workspace_pk` + metadatos.
3. Acceso: validar `X-Workspace` + membership role → permitir crear/leer/editar/borrar.
4. Relacionar recursos (issues, tasks) usando `project_pk` y `workspace_pk` para evitar fuga entre workspaces.
5. Ejemplo endpoint:
   - GET /workspaces/:workspace_pk/projects
   - POST /workspaces/:workspace_pk/projects
   - PATCH /workspaces/:workspace_pk/projects/:project_pk

Notas finales:

- Centralizar validaciones de workspace en middleware para consistencia.
- Considerar RLS para mayor seguridad a nivel DB.
- Auditar acciones críticas (create/delete/invite).
- Mantener contratos de API claros sobre el uso de `X-Workspace`.
