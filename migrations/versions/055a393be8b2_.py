"""empty message

Revision ID: 055a393be8b2
Revises: 4fd555443891
Create Date: 2021-08-03 17:14:16.219937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '055a393be8b2'
down_revision = '4fd555443891'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('broadcasts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('broadcast', sa.String(), nullable=False),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_broadcasts_timestamp'), 'broadcasts', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_broadcasts_timestamp'), table_name='broadcasts')
    op.drop_table('broadcasts')
    # ### end Alembic commands ###
