"""add workspace role enum

Revision ID: 0005
Revises: 0004
Create Date: 2026-01-02 16:21:30.027394

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0005"
down_revision: Union[str, Sequence[str], None] = "0004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create the enum type
    workspacerole = sa.Enum("OWNER", "ADMIN", "MEMBER", "VIEWER", name="workspacerole")
    workspacerole.create(op.get_bind(), checkfirst=True)

    # Update existing rows to use uppercase values
    op.execute("UPDATE workspace_member SET role = UPPER(role)")

    # Alter column to use enum type
    op.alter_column(
        "workspace_member",
        "role",
        existing_type=sa.VARCHAR(),
        type_=workspacerole,
        nullable=False,
        postgresql_using="role::text::workspacerole",
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Alter column back to VARCHAR
    op.alter_column(
        "workspace_member",
        "role",
        existing_type=sa.Enum(
            "OWNER", "ADMIN", "MEMBER", "VIEWER", name="workspacerole"
        ),
        type_=sa.VARCHAR(),
        nullable=True,
    )

    # Update values to lowercase
    op.execute("UPDATE workspace_member SET role = LOWER(role)")

    # Drop the enum type
    sa.Enum("OWNER", "ADMIN", "MEMBER", "VIEWER", name="workspacerole").drop(
        op.get_bind(), checkfirst=True
    )
