from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from supabase_auth import User

from app.core.security import ALGORITHM, SECRET_KEY
from app.db.session import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Module-level dependency objects to avoid calling Depends() in function signatures
OAUTH2_SCHEME_DEP = Depends(oauth2_scheme)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# DB dependency object must be created after `get_db` is defined
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
