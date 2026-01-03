from uuid import UUID

from pydantic import BaseModel, ConfigDict


class WorkspaceMemberRead(BaseModel):
    pk: UUID
    user: UUID
    workspace: UUID
    role: str
    model_config: ConfigDict = {"from_attributes": True}


class WorkspaceMemeberUpdateRole(BaseModel):
    role: str
