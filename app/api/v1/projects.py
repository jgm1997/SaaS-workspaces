from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.api.constants import DB_DEP, PROJECT_NOT_FOUND, USER_DEP, WORKSPACE_DEP
from app.models.user import User
from app.models.workspace import Workspace
from app.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate
from app.services.project_service import (
    create_project,
    delete_project,
    get_project,
    list_projects,
    update_project,
)

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectRead)
def cretate_project_endpoint(
    data: ProjectCreate,
    db: Session = DB_DEP,
    user: User = USER_DEP,
    workspace: Workspace = WORKSPACE_DEP,
):
    return create_project(db, workspace, data.name, data.description)


@router.get("", response_model=list[ProjectRead])
def list_projects_endpoint(
    db: Session = DB_DEP, user: User = USER_DEP, workspace: Workspace = WORKSPACE_DEP
):
    return list_projects(db, workspace)


@router.get("/{project_pk}", response_model=ProjectRead)
def get_project_endpoint(
    project_pk: str,
    db: Session = DB_DEP,
    user: User = USER_DEP,
    workspace: Workspace = WORKSPACE_DEP,
):
    project = get_project(db, workspace, project_pk)
    if not project:
        raise HTTPException(status_code=404, detail=PROJECT_NOT_FOUND)
    return project


@router.put("/{project_pk}", response_model=ProjectRead)
def update_project_endpoint(
    project_pk: str,
    data: ProjectUpdate,
    db: Session = DB_DEP,
    user: User = USER_DEP,
    workspace: Workspace = WORKSPACE_DEP,
):
    project = update_project(db, workspace, project_pk, data.name, data.description)
    if not project:
        raise HTTPException(status_code=404, detail=PROJECT_NOT_FOUND)
    return project


@router.delete("/{project_pk}")
def delete_project_endpoint(
    project_pk: str,
    db: Session = DB_DEP,
    user: User = USER_DEP,
    workspace: Workspace = WORKSPACE_DEP,
):
    ok = delete_project(db, workspace, project_pk)
    if not ok:
        raise HTTPException(status_code=404, detail=PROJECT_NOT_FOUND)
    return {"status": "deleted"}
