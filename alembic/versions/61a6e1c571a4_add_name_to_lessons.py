"""add_name_to_lessons

Revision ID: 61a6e1c571a4
Revises: 62e03fcbb4d2
Create Date: 2024-08-22 21:43:17.035555

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '61a6e1c571a4'
down_revision: Union[str, None] = '62e03fcbb4d2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lessons', sa.Column('name', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lessons', 'name')
    # ### end Alembic commands ###
