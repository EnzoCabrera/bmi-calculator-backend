"""Creating relationship between diets and users. Configuring for the method that creates diets.

Revision ID: 2d034c20b4a1
Revises: 1ff645908814
Create Date: 2025-04-08 10:44:00.128167

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d034c20b4a1'
down_revision: Union[str, None] = '1ff645908814'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('diets', sa.Column('user_id', sa.Integer(), nullable=True))
    op.alter_column('diets', 'description',
               existing_type=sa.VARCHAR(),
               type_=sa.Text(),
               existing_nullable=False)
    op.alter_column('diets', 'image_path',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.create_foreign_key(None, 'diets', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'diets', type_='foreignkey')
    op.alter_column('diets', 'image_path',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('diets', 'description',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    op.drop_column('diets', 'user_id')
    # ### end Alembic commands ###
