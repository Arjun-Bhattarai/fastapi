"""init

Revision ID: ebc18997bef8
Revises: 
Create Date: 2026-03-15 21:55:51.718772

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel 

from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ebc18997bef8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users',
    sa.Column('uid', sa.UUID(), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('first_name', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('last_name', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('create_at', postgresql.TIMESTAMP(), nullable=True),
    sa.Column('update_at', postgresql.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.alter_column('books', 'publish_date',
               existing_type=sa.VARCHAR(),
               type_=sa.DateTime(),
               existing_nullable=False,
               postgresql_using="publish_date::timestamp without time zone")  # add this


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column('books', 'publish_date',
               existing_type=sa.DateTime(),
               type_=sa.VARCHAR(),
               existing_nullable=False,
               postgresql_using="publish_date::varchar")  # add this too
    op.drop_table('users')