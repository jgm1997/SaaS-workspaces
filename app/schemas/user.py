from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr
    is_active: bool = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserRead(UserBase):
    pk: UUID
    model_config: ConfigDict = {"from_attributes": True}
