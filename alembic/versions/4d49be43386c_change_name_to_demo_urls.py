"""change_name_to_demo_urls

Revision ID: 4d49be43386c
Revises: 4ddd2e14d1f6
Create Date: 2024-09-07 12:20:16.593333

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '4d49be43386c'
down_revision: Union[str, None] = '4ddd2e14d1f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lessons', sa.Column('demo_urls', postgresql.ARRAY(sa.String()), nullable=True))
    op.drop_column('lessons', 'voice_urls')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lessons', sa.Column('voice_urls', postgresql.ARRAY(sa.VARCHAR()), autoincrement=False, nullable=True))
    op.drop_column('lessons', 'demo_urls')
    # ### end Alembic commands ###
