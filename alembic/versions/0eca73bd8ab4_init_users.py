"""init users (baseline stamp)

Revision ID: 0eca73bd8ab4
Revises:
Create Date: 2026-05-19 16:33:45.095545

DB schema already exists via create_all / manual setup.
This revision only registers the Alembic baseline (no DDL).
"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "0eca73bd8ab4"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
