# Public API Documentation — SaaS Workspaces

## Introduction

This API allows external clients to interact with your multi‑tenant workspace platform.
All operations are performed within the context of a workspace, selected via the `X-Workspace` header.

The API is **RESTful**, uses **JSON**, and requires **Bearer Token authentication**.

Base URL:

```plaintext
https://api.your-saas.com
```

(Development: `http://localhost:8000`)

## Technologies used

- `Python >= 3.11`
- `FastAPI >= 0.115.0`
- `PostgreSQL >= 15`
- `SQLAlchemy >= 2.0.45`
- `Alembic >= 1.17.2`
- `Pytest >= 8.0.0`
- `Poetry >= 2.0.0`

---

## Authentication

### Register a user

#### POST /auth/register

Creates a new user.

##### Request body (register)

```json
{
  "email": "user@example.com",
  "password": "secret123"
}
```

##### Response (List workspaces)

```json
{
  "pk": "uuid",
  "email": "user@example.com",
  "is_active": true
}
```

---

### Login

#### POST /auth/login

Returns a JWT access token.

##### Request body (login)

```json
{
  "email": "user@example.com",
  "password": "secret123"
}
```

##### Response

```json
{
  "access_token": "jwt-token",
  "token_type": "bearer"
}
```

---

## Authentication in requests

All protected endpoints require:

```plaintext
Authorization: Bearer <token>
```

---

### Workspace Selection

The API is multi‑tenant.
To operate inside a workspace, you must send:

```plaintext
X-Workspace: <workspace_pk>
```

If missing, the API returns:

```json
{
  "detail": "X-Workspace header missing"
}
```

---

## Workspaces

### Create a workspace

#### POST /workspaces

##### Request body (create workspace)

```json
{
  "name": "My Workspace"
}
```

##### Response (create workspace)

```json
{
  "pk": "uuid",
  "name": "My Workspace"
}
```

---

### List user workspaces

#### GET /workspaces

##### Response (list workspaces)

```json
[
  {
    "pk": "uuid",
    "name": "My Workspace"
  }
]
```

---

## Projects

All project endpoints require:

- `Authorization: Bearer <token>`
- `X-Workspace: <workspace_pk>`

---

### Create a project

#### POST /projects

##### Request body (create project)

```json
{
  "name": "Project A",
  "description": "Optional description"
}
```

##### Response (creat project)

```json
{
  "pk": "uuid",
  "name": "Project A",
  "description": "Optional description",
  "workspace": "uuid"
}
```

---

### List projects

#### GET /projects

##### Response (list projects)

```json
[
  {
    "pk": "uuid",
    "name": "Project A",
    "description": "Optional description",
    "workspace": "uuid"
  }
]
```

---

### Get a project

#### GET /projects/{project_pk}

---

### Update a project

#### PUT /projects/{project_pk}

##### Request body (update project)

```json
{
  "name": "New name",
  "description": "Updated description"
}
```

---

### Delete a project

#### DELETE /projects/{project_pk}

---

## Invitations

### Invite a user

#### POST /invitations

Requires role `owner` or `admin`.

##### Request body (invite user)

```json
{
  "email": "invitee@example.com"
}
```

##### Response (invite user)

```json
{
  "pk": "uuid",
  "email": "invitee@example.com",
  "workspace": "uuid",
  "invited_by": "uuid",
  "accepted": false
}
```

---

### Accept an invitation

#### POST /invitations/{invitation_pk}/accept

---

## Workspace Members

### List members

#### GET /members

##### Response (list members)

```json
[
  {
    "pk": "uuid",
    "user": "uuid",
    "workspace": "uuid",
    "role": "owner"
  }
]
```

---

### Change a member’s role

#### PATCH /members/{member_pk}/role

Requires role `owner` or `admin`.

##### Request body (change member role)

```json
{
  "role": "admin"
}
```

---

### Remove a member

#### DELETE /members/{member_pk}

Requires role `owner` or `admin`.

---

## Common Errors

### 400 — Bad Request

- Invalid data
- Email already registered
- Invitation already accepted

### 401 — Unauthorized

- Invalid token
- Expired token

### 403 — Forbidden

- Insufficient permissions
- Attempt to modify the owner without being owner

### 404 — Not Found

- Workspace not found
- Project not found
- Member not found

### 429 — Too Many Requests

- Rate limiting triggered

---

## API Conventions

- All primary keys are UUIDs and named `pk`.
- All tables use singular names.
- Foreign keys are named after the referenced table.
- The API is strictly multi‑tenant via `X-Workspace`.
- Roles define permissions:
  - `owner`
  - `admin`
  - `member`
  - `viewer`
