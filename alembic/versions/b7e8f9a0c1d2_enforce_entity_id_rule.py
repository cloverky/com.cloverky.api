"""enforce ENTITY_RULE: int PK column id, drop legacy secom_users

Revision ID: b7e8f9a0c1d2
Revises: a1813bb87835
Create Date: 2026-05-19

docs/DevOps/Backend/ENTITY_RULE.md
"""

from typing import Sequence, Union

from alembic import op

revision: str = "b7e8f9a0c1d2"
down_revision: Union[str, Sequence[str], None] = "a1813bb87835"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("DROP TABLE IF EXISTS secom_users CASCADE")


def downgrade() -> None:
    pass
