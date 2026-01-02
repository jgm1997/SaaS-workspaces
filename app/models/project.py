import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Project(Base):
    __tablename__ = "project"

    pk = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    workspace = Column(
        UUID(as_uuid=True),
        ForeignKey("workspace.pk", ondelete="CASCADE"),
        nullable=False,
    )
    workspace_rel = relationship("Workspace")
