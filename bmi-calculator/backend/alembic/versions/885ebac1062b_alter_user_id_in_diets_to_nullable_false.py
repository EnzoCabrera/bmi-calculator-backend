"""Alter user_id in diets to nullable=False

Revision ID: 885ebac1062b
Revises: 2d034c20b4a1
Create Date: 2025-04-08 10:56:27.626777

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '885ebac1062b'
down_revision: Union[str, None] = '2d034c20b4a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('diets', 'user_id',
               existing_type=sa.Integer(),
               nullable=False)



def downgrade() -> None:
    op.alter_column('diets', 'user_id',
               existing_type=sa.Integer(),
               nullable=True)

