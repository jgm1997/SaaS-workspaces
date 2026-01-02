from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from app.api.constants import DB_DEP
from app.schemas.auth import LoginRequest, Token
from app.schemas.user import UserCreate, UserRead
from app.services.auth_service import authenticate_user, register_user

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead)
def register(data: UserCreate, db: Session = DB_DEP):
    try:
        return register_user(db, data.email, data.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/login")
def login(data: LoginRequest, db: Session = DB_DEP):
    try:
        token = authenticate_user(db, data.email, data.password)
        return Token(access_token=token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail="Invalid credentials") from e
