"""add contents column to posts table

Revision ID: a263fbcfe502
Revises: 8cac140c0a9f
Create Date: 2024-04-24 15:31:34.277819

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a263fbcfe502'
down_revision: Union[str, None] = '8cac140c0a9f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('contents', sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column('posts', 'contents')
