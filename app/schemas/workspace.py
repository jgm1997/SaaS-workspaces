from uuid import UUID

from pydantic import BaseModel


class WorkspaceBase(BaseModel):
    name: str


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceRead(WorkspaceBase):
    pk: UUID

    class Config:
        from_attributes = True
