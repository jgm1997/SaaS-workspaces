import uuid

from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base


class Invitation(Base):
    __tablename__ = "invitation"

    pk = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False
    )
    email = Column(String, nullable=False)
    workspace = Column(
        UUID(as_uuid=True),
        ForeignKey("workspace.pk", ondelete="CASCADE"),
        nullable=False,
    )
    invited_by = Column(
        UUID(as_uuid=True), ForeignKey("user.pk", ondelete="SET NULL"), nullable=True
    )
    accepted = Column(Boolean, default=False)

    workspace_rel = relationship("Workspace")
    invited_by_rel = relationship("User")
