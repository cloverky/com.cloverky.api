"""codes 제거 · receipts / receipt_lines 추가 (영수증 파싱, 이미지 미저장)

Revision ID: e7f8a9b0c1d2
Revises: d9e1f2a3b4c5
Create Date: 2026-05-21
"""

from collections.abc import Sequence

from alembic import op

revision: str = "e7f8a9b0c1d2"
down_revision: str | Sequence[str] | None = "d9e1f2a3b4c5"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("DROP TABLE IF EXISTS codes CASCADE;")
    op.execute("DROP TABLE IF EXISTS fridge_codes CASCADE;")

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS receipts (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL
                REFERENCES users (id) ON DELETE CASCADE,
            store_name VARCHAR(200),
            purchased_date DATE,
            status VARCHAR(20) NOT NULL DEFAULT 'parsed',
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )
    op.execute("CREATE INDEX IF NOT EXISTS ix_receipts_user_id ON receipts (user_id);")

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS receipt_lines (
            id SERIAL PRIMARY KEY,
            receipt_id INTEGER NOT NULL
                REFERENCES receipts (id) ON DELETE CASCADE,
            line_name VARCHAR(200) NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 1,
            unit VARCHAR(20) NOT NULL DEFAULT '개',
            food_id INTEGER
                REFERENCES foods (id) ON DELETE SET NULL,
            inventory_id INTEGER
                REFERENCES inventory (id) ON DELETE SET NULL,
            raw_text TEXT
        );
        """
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_receipt_lines_receipt_id ON receipt_lines (receipt_id);",
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_receipt_lines_food_id ON receipt_lines (food_id);",
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS ix_receipt_lines_inventory_id ON receipt_lines (inventory_id);",
    )


def downgrade() -> None:
    op.execute("DROP TABLE IF EXISTS receipt_lines CASCADE;")
    op.execute("DROP TABLE IF EXISTS receipts CASCADE;")

    op.execute(
        """
        CREATE TABLE IF NOT EXISTS codes (
            id SERIAL PRIMARY KEY,
            food_id INTEGER NOT NULL
                REFERENCES foods (id) ON DELETE CASCADE,
            code VARCHAR(64) NOT NULL,
            code_type VARCHAR(32) NOT NULL DEFAULT 'barcode',
            created_at TIMESTAMPTZ NOT NULL DEFAULT now()
        );
        """
    )
    op.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_codes_code ON codes (code);")
    op.execute("CREATE INDEX IF NOT EXISTS ix_codes_food_id ON codes (food_id);")
