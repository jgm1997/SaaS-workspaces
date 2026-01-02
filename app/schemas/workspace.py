from uuid import UUID

from pydantic import BaseModel, ConfigDict


class WorkspaceBase(BaseModel):
    name: str


class WorkspaceCreate(WorkspaceBase):
    pass


class WorkspaceRead(WorkspaceBase):
    pk: UUID
    model_config: ConfigDict = {"from_attributes": True}
