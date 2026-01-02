from sqlalchemy.orm import Session

from app.models.invitation import Invitation
from app.models.user import User
from app.models.workspace import Workspace, WorkspaceMember, WorkspaceRole


def user_can_invite(db: Session, user: User, workspace: Workspace) -> bool:
    membership = (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.user == user.pk, WorkspaceMember.workspace == workspace.pk
        )
        .first()
    )
    if not membership:
        return False

    return membership.role in (WorkspaceRole.OWNER, WorkspaceRole.ADMIN)


def create_invitation(
    db: Session, workspace: Workspace, invited_by: User, email: str
) -> Invitation:
    invitation = Invitation(
        email=email, workspace=workspace.pk, invited_by=invited_by.pk
    )
    db.add(invitation)
    db.commit()
    db.refresh(invitation)
    return invitation


def accept_invitation(db: Session, invitation: Invitation, user: User) -> None:
    invitation.accepted = True
    membership = WorkspaceMember(
        user=user.pk, workspace=invitation.workspace, role=WorkspaceRole.MEMBER
    )
    db.add(membership)
    db.commit()
