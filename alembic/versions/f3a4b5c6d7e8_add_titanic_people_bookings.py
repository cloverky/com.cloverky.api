"""titanic people / bookings (James PersonCommand·BookingCommand)

Revision ID: f3a4b5c6d7e8
Revises: e7f8a9b0c1d2
Create Date: 2026-06-04
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "f3a4b5c6d7e8"
down_revision: Union[str, Sequence[str], None] = "e7f8a9b0c1d2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "people",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("passenger_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("gender", sa.String(length=20), nullable=False, server_default=""),
        sa.Column("age", sa.Numeric(8, 2), nullable=True),
        sa.Column("sib_sp", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("parch", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("survived", sa.Integer(), nullable=False, server_default="0"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("passenger_id"),
    )
    op.create_index("ix_people_passenger_id", "people", ["passenger_id"], unique=False)

    op.create_table(
        "bookings",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("person_id", sa.BigInteger(), nullable=False),
        sa.Column("pclass", sa.Integer(), nullable=False, server_default="3"),
        sa.Column("ticket", sa.String(length=128), nullable=False, server_default=""),
        sa.Column("fare", sa.Numeric(12, 4), nullable=False, server_default="0"),
        sa.Column("cabin", sa.String(length=64), nullable=True),
        sa.Column("embarked", sa.String(length=8), nullable=True),
        sa.ForeignKeyConstraint(["person_id"], ["people.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("person_id"),
    )
    op.create_index("ix_bookings_person_id", "bookings", ["person_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_bookings_person_id", table_name="bookings")
    op.drop_table("bookings")
    op.drop_index("ix_people_passenger_id", table_name="people")
    op.drop_table("people")
