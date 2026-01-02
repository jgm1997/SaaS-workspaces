from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID


def _get_utc_now():
    return datetime.now(timezone.utc)


class AuditMixin:
    created_at = Column(DateTime, default=_get_utc_now, nullable=False)
    updated_at = Column(
        DateTime,
        default=_get_utc_now,
        onupdate=_get_utc_now,
    )

    created_by = Column(UUID(as_uuid=True), ForeignKey("user.pk"), nullable=True)
    updated_by = Column(UUID(as_uuid=True), ForeignKey("user.pk"), nullable=True)
