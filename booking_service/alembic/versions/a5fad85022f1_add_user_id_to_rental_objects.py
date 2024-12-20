"""Add user_id to rental_objects

Revision ID: a5fad85022f1
Revises: bdc053d30300
Create Date: 2024-12-08 01:32:07.025390

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5fad85022f1'
down_revision: Union[str, None] = 'bdc053d30300'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rental_objects', sa.Column('user_id', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rental_objects', 'user_id')
    # ### end Alembic commands ###
