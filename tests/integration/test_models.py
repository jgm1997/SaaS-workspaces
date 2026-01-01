from uuid import UUID, uuid4

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.user import User
from app.models.workspace import Workspace, WorkspaceMember


def test_create_user_workspace_membership() -> None:
    db: Session = SessionLocal()

    user = User(email=f"test+{uuid4()}@example.com", hashed_password="hashed")
    db.add(user)
    db.commit()
    db.refresh(user)

    workspace = Workspace(name=f"Test Workspace {uuid4()}")
    db.add(workspace)
    db.commit()
    db.refresh(workspace)

    membership = WorkspaceMember(
        user=user.pk,
        workspace=workspace.pk,
        role="owner",
    )
    db.add(membership)
    db.commit()
    db.refresh(membership)

    assert isinstance(user.pk, UUID)
    assert isinstance(workspace.pk, UUID)
    assert membership.user == user.pk
    assert membership.workspace == workspace.pk
