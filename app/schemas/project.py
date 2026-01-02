from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ProjectBase(BaseModel):
    name: str
    description: str | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    name: str | None = None
    description: str | None = None


class ProjectRead(ProjectBase):
    pk: UUID
    workspace: UUID
    model_config: ConfigDict = {"from_attributes": True}
