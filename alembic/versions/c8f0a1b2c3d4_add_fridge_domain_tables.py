"""add fridge domain tables (Neon public schema)

Revision ID: c8f0a1b2c3d4
Revises: b7e8f9a0c1d2
Create Date: 2026-05-20

backend/apps/fridge/models 와 동일 스키마.
"""

from collections.abc import Sequence

from alembic import op

revision: str = "c8f0a1b2c3d4"
down_revision: str | Sequence[str] | None = "b7e8f9a0c1d2"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # IF NOT EXISTS — 앱 create_all 과 중복 실행돼도 안전
    op.execute(
        """
        CREATE TABLE IF NOT EXISTS fridge_categories (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            sort_order INTEGER NOT NULL DEFAULT 0,
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )
    op.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS ix_fridge_categories_name "
        "ON fridge_categories (name);",
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS fridge_foods (
            id SERIAL PRIMARY KEY,
            category_id INTEGER NOT NULL
                REFERENCES fridge_categories (id) ON DELETE RESTRICT,
            name VARCHAR(200) NOT NULL,
            description TEXT,
            default_unit VARCHAR(20) NOT NULL DEFAULT '개',
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_fridge_foods_category_id ON fridge_foods (category_id);",
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_fridge_foods_name ON fridge_foods (name);",
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS fridge_codes (
            id SERIAL PRIMARY KEY,
            food_id INTEGER NOT NULL
                REFERENCES fridge_foods (id) ON DELETE CASCADE,
            code VARCHAR(64) NOT NULL,
            code_type VARCHAR(32) NOT NULL DEFAULT 'barcode',
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )
    op.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS ix_fridge_codes_code ON fridge_codes (code);",
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_fridge_codes_food_id ON fridge_codes (food_id);",
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS fridge_users (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL UNIQUE
                REFERENCES users (id) ON DELETE CASCADE,
            default_storage VARCHAR(20) NOT NULL DEFAULT '냉장',
            created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_fridge_users_user_id ON fridge_users (user_id);",
    )

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS fridge_inventory (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL
                REFERENCES users (id) ON DELETE CASCADE,
            food_id INTEGER NOT NULL
                REFERENCES fridge_foods (id) ON DELETE CASCADE,
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
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_fridge_inventory_user_id ON fridge_inventory (user_id);",
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_fridge_inventory_food_id ON fridge_inventory (food_id);",
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS fridge_inventory CASCADE;")
    op.execute("DROP TABLE IF EXISTS fridge_users CASCADE;")
    op.execute("DROP TABLE IF EXISTS fridge_codes CASCADE;")
    op.execute("DROP TABLE IF EXISTS fridge_foods CASCADE;")
    op.execute("DROP TABLE IF EXISTS fridge_categories CASCADE;")
