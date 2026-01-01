"""initial empty migration

Revision ID: 2883bccc7222
Revises: 280e67ddaad6
Create Date: 2026-01-01 20:05:02.258964

"""

from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = "2883bccc7222"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
