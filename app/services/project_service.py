from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.workspace import Workspace


def create_project(
    db: Session, workspace: Workspace, name: str, description: str | None = None
) -> Project:
    project = Project(name=name, description=description, workspace=workspace.pk)
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
    project_pk: str,
    name: str | None,
    description: str | None,
) -> Project | None:
    project = get_project(db, workspace, project_pk)
    if not project:
        return None

    if name is not None:
        project.name = name
    if description is not None:
        project.description = description

    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, workspace: Workspace, project_pk: str) -> bool:
    project = get_project(db, workspace, project_pk)
    if not project:
        return False

    db.delete(project)
    db.commit()
    return True
