from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import DB_DEP, USER_DEP, WORKSPACE_DEP
from app.models.user import User
from app.models.workspace import Workspace
from app.schemas.membership import WorkspaceMemberRead, WorkspaceMemeberUpdateRole
from app.services.membership_service import (
    change_memeber_role,
    list_members,
    remove_member,
)

router = APIRouter(prefix="/members", tags=["members"])


@router.get("", response_model=list[WorkspaceMemberRead])
def list_members_endpoint(
    db: Session = DB_DEP, user: User = USER_DEP, workspace: Workspace = WORKSPACE_DEP
):
    return list_members(db, workspace)


@router.patch("/{member_pk}/role", response_model=WorkspaceMemberRead)
def change_role_endpoint(
    member_pk: str,
    data: WorkspaceMemeberUpdateRole,
    db: Session = DB_DEP,
    user: User = USER_DEP,
    workspace: Workspace = WORKSPACE_DEP,
):
    try:
        return change_memeber_role(db, user, workspace, member_pk, data.role)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.delete("/{member_pk}")
def remove_member_endpoint(
    member_pk: str,
    db: Session = DB_DEP,
    user: User = USER_DEP,
    workspace: Workspace = WORKSPACE_DEP,
):
    try:
        remove_member(db, user, workspace, member_pk)
        return {"status": "removed"}
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
