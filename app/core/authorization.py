from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.project import Project
from app.models.user import User
from app.models.workspace import Workspace, WorkspaceMember


def get_membership(
    db: Session, user: User, workspace: Workspace
) -> WorkspaceMember | None:
    return (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.user == user.pk, WorkspaceMember.workspace == workspace.pk
        )
        .first()
    )


def require_role(membership: WorkspaceMember, allowed: list[str]) -> None:
    if membership.role not in allowed:
        raise PermissionError(f"Role {membership.role} not allowed")


def can_create_project(db: Session, user: User, workspace: Workspace) -> bool:
    membership = get_membership(db, user, workspace)
    if not membership:
        return False
    return membership.role in ("owner", "admin", "member")


def can_edit_project(
    db: Session, user: User, workspace: Workspace, project: Project
) -> bool:
    membership = get_membership(db, user, workspace)
    if not membership:
        return False

    if membership.role in ("owner", "admin"):
        return True

    if membership.role == "member" and project.workspace == workspace.pk:
        return True
    return False


def can_delete_project(
    db: Session, user: User, workspace: Workspace, project: Project
) -> bool:
    membership = get_membership(db, user, workspace)
    if not membership:
        return False
    if project.workspace != workspace.pk:
        raise HTTPException(status_code=404, detail="Project not found")
    return membership.role in ("owner", "admin")
