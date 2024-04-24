"""add published and created_at columns in posts table

Revision ID: ff45b1b343fb
Revises: e95b4b383b5e
Create Date: 2024-04-24 16:00:37.782281

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff45b1b343fb'
down_revision: Union[str, None] = 'e95b4b383b5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
        op.add_column(
            'posts', 
            sa.Column(
                'published', 
                sa.BOOLEAN(), 
                server_default='TRUE', 
                nullable=False
            )
        ),
        op.add_column(
            'posts', 
            sa.Column(
                'created_at', 
                sa.TIMESTAMP(timezone=True), 
                server_default=sa.text('now()'), 
                nullable=False
            )
        )


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
