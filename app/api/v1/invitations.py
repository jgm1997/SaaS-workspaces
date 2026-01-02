from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.api.constants import INVITATION_DEP, USER_DEP, WORKSPACE_DEP
from app.api.deps import DB_DEP
from app.models.invitation import Invitation
from app.models.user import User
from app.models.workspace import Workspace
from app.schemas.invitation import InvitationCreate, InvitationRead
from app.services.invitation_service import (
    accept_invitation,
    create_invitation,
    user_can_invite,
)

router = APIRouter(prefix="/invitations", tags=["invitations"])


@router.post("", response_model=InvitationRead)
def invite_user(
    data: InvitationCreate,
    db: Session = DB_DEP,
    user: User = USER_DEP,
    workspace: Workspace = WORKSPACE_DEP,
):
    if not user_can_invite(db, user, workspace):
        raise HTTPException(
            status_code=403,
            detail="User does not have permission to invite users to this workspace.",
        )
    return create_invitation(db, workspace, user, data.email)


@router.post("/{invitation_pk}/accept")
def accept_invitation_endpoint(
    invitation: Invitation = INVITATION_DEP, db: Session = DB_DEP, user: User = USER_DEP
):
    if invitation.email != user.email:
        raise HTTPException(
            status_code=403, detail="This invitation is not for the current user."
        )
    if invitation.accepted:
        raise HTTPException(
            status_code=400, detail="Invitation has already been accepted."
        )
    accept_invitation(db, invitation, user)
    return {"status": "accepted"}
