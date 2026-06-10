"""people 테이블명을 person 으로 변경

Revision ID: g4b5c6d7e8f9
Revises: f3a4b5c6d7e8
Create Date: 2026-06-04
"""

from typing import Sequence, Union

from alembic import op
from sqlalchemy import inspect

revision: str = "g4b5c6d7e8f9"
down_revision: Union[str, Sequence[str], None] = "f3a4b5c6d7e8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    tables = set(inspect(op.get_bind()).get_table_names())
    if "people" not in tables:
        return
    op.rename_table("people", "person")
    op.execute("ALTER INDEX IF EXISTS ix_people_passenger_id RENAME TO ix_person_passenger_id")


def downgrade() -> None:
    tables = set(inspect(op.get_bind()).get_table_names())
    if "person" not in tables:
        return
    op.execute("ALTER INDEX IF EXISTS ix_person_passenger_id RENAME TO ix_people_passenger_id")
    op.rename_table("person", "people")
