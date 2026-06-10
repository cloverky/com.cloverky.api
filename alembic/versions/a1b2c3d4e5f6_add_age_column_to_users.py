"""add age column to users table

Revision ID: a1b2c3d4e5f6
Revises: 0eca73bd8ab4
Create Date: 2026-05-19 16:40:00.000000

"""

from typing import Sequence, Union

from alembic import op

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, Sequence[str], None] = "0eca73bd8ab4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # create_all 등으로 이미 age 가 있을 수 있음 (Neon 등)
    op.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS age INTEGER")


def downgrade() -> None:
    op.drop_column("users", "age")
