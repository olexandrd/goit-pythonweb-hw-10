"""add  field confirmed to User model

Revision ID: f0edb9af561e
Revises: 466637aea20b
Create Date: 2024-11-27 20:08:05.387126

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0edb9af561e'
down_revision: Union[str, None] = '466637aea20b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###