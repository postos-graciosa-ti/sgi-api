"""add teste field at workers table

Revision ID: 741891b5ae5a
Revises:
Create Date: 2025-03-21 09:51:12.713523

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "741891b5ae5a"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("workers", sa.Column("teste", sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("workers", "teste")
