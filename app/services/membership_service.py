from sqlalchemy.orm import Session

from app.core.authorization import get_membership
from app.models.user import User
from app.models.workspace import Workspace, WorkspaceMember


def list_members(db: Session, workspace: Workspace) -> list[Workspace]:
    return (
        db.query(WorkspaceMember)
        .filter(WorkspaceMember.workspace == workspace.pk)
        .all()
    )


def change_memeber_role(
    db: Session, acting_user: User, workspace: Workspace, member_pk: str, new_role: str
) -> WorkspaceMember:
    acting_membership = get_membership(db, acting_user, workspace)
    if not acting_membership or acting_membership.role not in ("owner", "admin"):
        raise PermissionError("Not allowed to change roles.")

    member = (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.pk == member_pk, WorkspaceMember.workspace == workspace.pk
        )
        .first()
    )
    if not member:
        raise ValueError("Member not found.")
    if member.role == "owner" and acting_membership.role != "owner":
        raise PermissionError("Only owner can modify ownership.")

    member.role = new_role
    db.commit()
    db.refresh(member)
    return member


def remove_member(
    db: Session, acting_user: User, workspace: Workspace, member_pk: str
) -> None:
    acting_membership = get_membership(db, acting_user, workspace)
    if not acting_membership or acting_membership.role not in ("owner", "admin"):
        raise PermissionError("Not allowed to remove members.")

    member = (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.pk == member_pk, WorkspaceMember.workspace == workspace.pk
        )
        .first()
    )
    if not member:
        raise ValueError("Member not found.")
    if member.role == "owner" and acting_membership.role != "owner":
        raise PermissionError("Only owners can remove owners.")

    db.delete(member)
    db.commit()
