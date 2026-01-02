from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.authorization import (
    can_create_project,
    can_delete_project,
    can_edit_project,
)
from app.models.project import Project
from app.models.user import User
from app.models.workspace import Workspace


def create_project(
    db: Session,
    workspace: Workspace,
    user: User,
    name: str,
    description: str | None = None,
) -> Project:
    project = Project(name=name, description=description, workspace=workspace.pk)
    if not can_create_project(db, user, workspace):
        raise PermissionError("User cannot create project in this workspace")
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def list_projects(db: Session, workspace: Workspace) -> list[Project]:
    return db.query(Project).filter(Project.workspace == workspace.pk).all()


def get_project(db: Session, workspace: Workspace, project_pk: str) -> Project | None:
    return (
        db.query(Project)
        .filter(Project.pk == project_pk, Project.workspace == workspace.pk)
        .first()
    )


def update_project(
    db: Session,
    workspace: Workspace,
    user: User,
    project_pk: str,
    name: str | None,
    description: str | None,
) -> Project | None:
    project = get_project(db, workspace, project_pk)
    if not project:
        return None

    if not can_edit_project(db, user, workspace, project):
        raise PermissionError("User cannot edit this project")

    if name is not None:
        project.name = name
    if description is not None:
        project.description = description

    db.commit()
    db.refresh(project)
    return project


def delete_project(
    db: Session, workspace: Workspace, user: User, project_pk: str
) -> bool:
    project = get_project(db, workspace, project_pk)
    if not project:
        return False

    if not can_delete_project(db, user, workspace, project):
        raise HTTPException(status_code=403, detail="User cannot delete this project")

    db.delete(project)
    db.commit()
    return True
