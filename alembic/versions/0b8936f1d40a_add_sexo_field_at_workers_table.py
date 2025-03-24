"""add sexo field at workers table

Revision ID: 0b8936f1d40a
Revises: 741891b5ae5a
Create Date: 2025-03-24 07:35:51.229478

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b8936f1d40a'
down_revision: Union[str, None] = '741891b5ae5a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("workers", sa.Column("sexo", sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("workers", "sexo")