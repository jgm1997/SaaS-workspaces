from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserRead(UserBase):
    pk: str

    class Config:
        from_attributes = True
