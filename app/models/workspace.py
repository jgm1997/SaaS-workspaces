import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Workspace(Base):
    __tablename__ = "workspace"

    pk = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    name = Column(String, unique=True, index=True, nullable=False)

    members = relationship("WorkspaceMember", back_populates="workspace_rel")


class WorkspaceMember(Base):
    __tablename__ = "workspace_member"

    pk = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    user = Column(
        UUID(as_uuid=True), ForeignKey("user.pk", ondelete="CASCADE"), nullable=False
    )
    workspace = Column(
        UUID(as_uuid=True),
        ForeignKey("workspace.pk", ondelete="CASCADE"),
        nullable=False,
    )
    role = Column(String, default="member")

    user_rel = relationship("User", back_populates="memberships")
    workspace_rel = relationship("Workspace", back_populates="members")
