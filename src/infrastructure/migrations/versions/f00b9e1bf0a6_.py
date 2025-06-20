"""empty message

Revision ID: f00b9e1bf0a6
Revises: 35bef3f301e6
Create Date: 2025-06-01 18:23:13.589623

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'f00b9e1bf0a6'
down_revision: Union[str, None] = '35bef3f301e6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    sa.Enum('PENDING', 'CONFIRMED', 'CANCALLED', 'COMPLETED', name='bookingstatus').create(op.get_bind())
    op.create_table('booking_tables',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('billiard_table_id', sa.Uuid(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.Column('status', postgresql.ENUM('PENDING', 'CONFIRMED', 'CANCALLED', 'COMPLETED', name='bookingstatus', create_type=False), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['billiard_table_id'], ['billiard_tables.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('booking_tables')
    sa.Enum('PENDING', 'CONFIRMED', 'CANCALLED', 'COMPLETED', name='bookingstatus').drop(op.get_bind())
    # ### end Alembic commands ###
