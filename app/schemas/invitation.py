from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr


class InvitationCreate(BaseModel):
    email: EmailStr


class InvitationRead(BaseModel):
    pk: UUID
    email: EmailStr
    workspace: UUID
    invited_by: UUID | None
    accepted: bool
    model_config: ConfigDict = {"from_attributes": True}
