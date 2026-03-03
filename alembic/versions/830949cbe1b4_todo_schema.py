"""todo_schema

Revision ID: 830949cbe1b4
Revises: 02cfa35bd81b
Create Date: 2026-03-03 22:08:17.680028

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '830949cbe1b4'
down_revision: Union[str, Sequence[str], None] = '02cfa35bd81b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'todos',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('content', sa.String(length=255), nullable=False),
        sa.Column('is_completed', sa.Text, nullable=True),
        sa.Column('created_at', sa.Boolean, default=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.now())
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('todos')