from fastapi import APIRouter
from sqlalchemy.orm import Session

from app.api.deps import CURRENT_USER_SCHEME, DB_DEP
from app.models.user import User
from app.schemas.workspace import WorkspaceCreate, WorkspaceRead
from app.services.workspace_service import _create_workspace, list_user_workspaces

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


@router.post("", response_model=WorkspaceRead)
def create_workspace(
    data: WorkspaceCreate,
    db: Session = DB_DEP,
    user: User = CURRENT_USER_SCHEME,
):
    return _create_workspace(db, user, data.name)


@router.get("", response_model=list[WorkspaceRead])
def list_ws(db: Session = DB_DEP, user: User = CURRENT_USER_SCHEME):
    return list_user_workspaces(db, user)
