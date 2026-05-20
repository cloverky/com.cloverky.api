"""add age column to users table

Revision ID: a1b2c3d4e5f6
Revises: 0eca73bd8ab4
Create Date: 2026-05-19 16:40:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "0eca73bd8ab4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("age", sa.Integer(), nullable=True))


def downgrade() -> None:
    op.drop_column("users", "age")
