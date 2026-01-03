from fastapi import APIRouter, HTTPException, Request
from sqlalchemy.orm import Session

from app.api.constants import PROJECT_NOT_FOUND
from app.api.deps import DB_DEP, USER_DEP, WORKSPACE_DEP
from app.core.rate_limit import limiter, workspace_key
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
@limiter.limit("30/minute", key_func=workspace_key)
def cretate_project_endpoint(
    data: ProjectCreate,
    request: Request,
    db: Session = DB_DEP,
    user: User = USER_DEP,
    workspace: Workspace = WORKSPACE_DEP,
):
    return create_project(db, workspace, user, data.name, data.description)


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
@limiter.limit("30/minute", key_func=workspace_key)
def update_project_endpoint(
    project_pk: str,
    data: ProjectUpdate,
    request: Request,
    db: Session = DB_DEP,
    user: User = USER_DEP,
    workspace: Workspace = WORKSPACE_DEP,
):
    project = update_project(
        db, workspace, user, project_pk, data.name, data.description
    )
    if not project:
        raise HTTPException(status_code=404, detail=PROJECT_NOT_FOUND)
    return project


@router.delete("/{project_pk}")
@limiter.limit("30/minute", key_func=workspace_key)
def delete_project_endpoint(
    project_pk: str,
    request: Request,
    db: Session = DB_DEP,
    user: User = USER_DEP,
    workspace: Workspace = WORKSPACE_DEP,
):
    ok = delete_project(db, workspace, user, project_pk)
    if not ok:
        raise HTTPException(status_code=404, detail=PROJECT_NOT_FOUND)
    return {"status": "deleted"}
