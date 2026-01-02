from sqlalchemy.orm import Session

from app.models.user import User
from app.models.workspace import Workspace, WorkspaceMember, WorkspaceRole


def _create_workspace(db: Session, user: User, name: str) -> Workspace:
    workspace = Workspace(name=name)
    db.add(workspace)
    db.commit()
    db.refresh(workspace)

    # Add the user as an owner of the workspace
    membership = WorkspaceMember(
        user=user.pk, workspace=workspace.pk, role=WorkspaceRole.OWNER
    )
    db.add(membership)
    db.commit()

    return workspace


def list_user_workspaces(db: Session, user: User) -> list[Workspace]:
    return (
        db.query(Workspace)
        .join(WorkspaceMember, Workspace.pk == WorkspaceMember.workspace)
        .filter(WorkspaceMember.user == user.pk)
        .all()
    )
