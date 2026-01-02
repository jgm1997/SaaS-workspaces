import uuid

from app.db.session import SessionLocal
from app.models.project import Project


def test_project_audit_fields(client, token):
    # Crear workspace
    unique_id = uuid.uuid4().hex[:8]
    workspace = client.post(
        "/workspaces", json={"name": f"WS-{unique_id}"}, headers=token
    ).json()
    workspace_pk = workspace["pk"]

    headers_ws = {
        "Authorization": token["Authorization"],
        "X-Workspace": workspace_pk,
    }

    # Crear project
    projects = client.post("/projects", json={"name": "Audit Test"}, headers=headers_ws)
    project = projects.json()

    assert "pk" in project
    assert "workspace" in project

    db = SessionLocal()
    project_query = db.query(Project).filter(Project.pk == project["pk"]).first()

    assert project_query.created_at is not None
    assert project_query.created_by is not None
