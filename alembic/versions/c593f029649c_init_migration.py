"""init_migration

Revision ID: c593f029649c
Revises:
Create Date: 2025-08-08 18:48:31.243528

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c593f029649c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id BIGINT NOT NULL ,
            name VARCHAR(255) NOT NULL,
            number BIGINT NOT NULL,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    op.execute("""
        CREATE TABLE IF NOT EXISTS programs (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            contact VARCHAR(255),
            plan JSONB,
            plan_hash VARCHAR(255)
        )
    """)


def downgrade() -> None:
    op.execute("""DROP TABLE IF EXISTS users""")
    op.execute("""DROP TABLE IF EXISTS programs""")
