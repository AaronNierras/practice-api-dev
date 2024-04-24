"""add foreign-key to posts table

Revision ID: e95b4b383b5e
Revises: d9dff1b63b96
Create Date: 2024-04-24 15:47:57.783782

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e95b4b383b5e'
down_revision: Union[str, None] = 'd9dff1b63b96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key(
        'posts_users_fk', 
        source_table='posts', referent_table='users', 
        local_cols=['user_id'], remote_cols=['id'], 
        ondelete='CASCADE'
    )


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
