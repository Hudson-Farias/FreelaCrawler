"""researches_table

Revision ID: 3d1b3b1597f8
Revises: 
Create Date: 2023-12-21 19:07:15.501391

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3d1b3b1597f8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None: op.create_table(
        'freelancers',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('search', sa.String(length=255), nullable=False),
        sa.Column('channel_id', sa.BIGINT(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('freelancers')