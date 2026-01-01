from uuid import UUID

from pydantic import BaseModel


class WorkspaceMemberRead(BaseModel):
    pk: UUID
    user: UUID
    workspace: UUID
    role: str

    class Config:
        from_attributes = True
