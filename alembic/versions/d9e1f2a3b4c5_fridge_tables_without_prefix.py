"""fridge_* 제거·users 단일화·도메인 테이블명 단순화 (alembic_version 유지)

Revision ID: d9e1f2a3b4c5
Revises: c8f0a1b2c3d4
Create Date: 2026-05-20
"""

from typing import Sequence, Union

from alembic import op

revision: str = "d9e1f2a3b4c5"
down_revision: Union[str, Sequence[str], None] = "c8f0a1b2c3d4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _drop_fridge_tables() -> None:
    for tbl in (
        "fridge_inventory",
        "fridge_codes",
        "fridge_foods",
        "fridge_categories",
        "fridge_users",
        "inventory",
        "codes",
        "foods",
        "categories",
    ):
        op.execute(f'DROP TABLE IF EXISTS "{tbl}" CASCADE')


def upgrade() -> None:
    _drop_fridge_tables()

    op.execute(
        "ALTER TABLE users ADD COLUMN IF NOT EXISTS default_storage VARCHAR(20) "
        "NOT NULL DEFAULT '냉장'",
    )

    op.execute(
        """
        CREATE TABLE categories (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            sort_order INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )
    op.execute("CREATE UNIQUE INDEX ix_categories_name ON categories (name);")

    op.execute(
        """
        CREATE TABLE foods (
            id SERIAL PRIMARY KEY,
            category_id INTEGER NOT NULL
                REFERENCES categories (id) ON DELETE RESTRICT,
            name VARCHAR(200) NOT NULL,
            description TEXT,
            default_unit VARCHAR(20) NOT NULL DEFAULT '개',
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )
    op.execute("CREATE INDEX ix_foods_category_id ON foods (category_id);")
    op.execute("CREATE INDEX ix_foods_name ON foods (name);")

    op.execute(
        """
        CREATE TABLE codes (
            id SERIAL PRIMARY KEY,
            food_id INTEGER NOT NULL
                REFERENCES foods (id) ON DELETE CASCADE,
            code VARCHAR(64) NOT NULL,
            code_type VARCHAR(32) NOT NULL DEFAULT 'barcode',
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )
    op.execute("CREATE UNIQUE INDEX ix_codes_code ON codes (code);")
    op.execute("CREATE INDEX ix_codes_food_id ON codes (food_id);")

    op.execute(
        """
        CREATE TABLE inventory (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL
                REFERENCES users (id) ON DELETE CASCADE,
            food_id INTEGER NOT NULL
                REFERENCES foods (id) ON DELETE CASCADE,
            quantity INTEGER NOT NULL DEFAULT 1,
            unit VARCHAR(20) NOT NULL DEFAULT '개',
            expiry_date DATE,
            purchased_date DATE,
            expiry_is_estimated BOOLEAN NOT NULL DEFAULT false,
            storage VARCHAR(20) NOT NULL DEFAULT '냉장',
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )
    op.execute("CREATE INDEX ix_inventory_user_id ON inventory (user_id);")
    op.execute("CREATE INDEX ix_inventory_food_id ON inventory (food_id);")


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS inventory CASCADE;")
    op.execute("DROP TABLE IF EXISTS codes CASCADE;")
    op.execute("DROP TABLE IF EXISTS foods CASCADE;")
    op.execute("DROP TABLE IF EXISTS categories CASCADE;")
    op.execute("ALTER TABLE users DROP COLUMN IF EXISTS default_storage;")
