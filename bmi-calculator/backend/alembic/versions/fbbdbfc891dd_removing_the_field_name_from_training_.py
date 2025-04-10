"""removing the field name from training and diets

Revision ID: fbbdbfc891dd
Revises: 3e31e61fe5f8
Create Date: 2025-03-29 13:06:22.147540

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fbbdbfc891dd'
down_revision: Union[str, None] = '3e31e61fe5f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('diets', 'name')
    op.drop_column('trainings', 'name')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('trainings', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.add_column('diets', sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
