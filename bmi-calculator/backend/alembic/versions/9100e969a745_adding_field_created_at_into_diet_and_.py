"""Adding field created_at into DIET and TRAINING tables

Revision ID: 9100e969a745
Revises: a27272e62c69
Create Date: 2025-05-15 22:50:24.101353

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '9100e969a745'
down_revision: Union[str, None] = 'a27272e62c69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_history_id', table_name='history')
    op.drop_table('history')
    op.add_column('diets', sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True))
    op.add_column('trainings', sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('now()'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('trainings', 'created_at')
    op.drop_column('diets', 'created_at')
    op.create_table('history',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('weight', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=False),
    sa.Column('bmi_value', sa.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='history_user_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='history_pkey')
    )
    op.create_index('ix_history_id', 'history', ['id'], unique=False)
    # ### end Alembic commands ###
