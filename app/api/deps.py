from fastapi import Depends, Header, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.security import ALGORITHM, SECRET_KEY
from app.db.session import SessionLocal
from app.models.invitation import Invitation
from app.models.user import User
from app.models.workspace import Workspace, WorkspaceMember

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


OAUTH2_SCHEME_DEP = Depends(oauth2_scheme)
DB_DEP = Depends(get_db)


def get_current_user(token: str = OAUTH2_SCHEME_DEP, db: Session = DB_DEP):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_pk = payload.get("sub")
    except JWTError as err:
        raise HTTPException(status_code=401, detail="Invalid token") from err

    user = db.query(User).filter(User.pk == user_pk).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


CURRENT_USER_SCHEME = Depends(get_current_user)


def get_current_workspace(
    x_workspace: str | None = Header(default=None, alias="X-Workspace"),
    db: Session = DB_DEP,
    user: User = CURRENT_USER_SCHEME,
) -> Workspace:
    if not x_workspace:
        raise HTTPException(status_code=400, detail="X-Workspace header missing.")

    workspace = db.query(Workspace).filter(Workspace.pk == x_workspace).first()
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace not found.")

    membership = (
        db.query(WorkspaceMember)
        .filter(
            WorkspaceMember.user == user.pk, WorkspaceMember.workspace == workspace.pk
        )
        .first()
    )
    if not membership:
        raise HTTPException(status_code=403, detail="Not a member of this workspace.")

    return workspace


def get_invitation(invitation_pk: str, db: Session = DB_DEP) -> Invitation:
    invitation = db.query(Invitation).filter(Invitation.pk == invitation_pk).first()
    if not invitation:
        raise HTTPException(status_code=404, detail="Invitation not found.")
    return invitation
