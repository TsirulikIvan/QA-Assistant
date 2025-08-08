"""add_first_last_name_to_users

Revision ID: 82fbefa0697b
Revises: c593f029649c
Create Date: 2025-08-08 19:07:32.585834
"""

from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "82fbefa0697b"
down_revision: Union[str, None] = "c593f029649c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
        ALTER TABLE users ADD COLUMN first_name VARCHAR(100);
    """)
    op.execute("""
        ALTER TABLE users ADD COLUMN last_name VARCHAR(100);
    """)


def downgrade() -> None:
    op.execute("""
        ALTER TABLE users DROP COLUMN last_name;
    """)
    op.execute("""
        ALTER TABLE users DROP COLUMN first_name;
    """)
