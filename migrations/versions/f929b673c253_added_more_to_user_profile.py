"""added more to user profile

Revision ID: f929b673c253
Revises: b79a7e23434f
Create Date: 2021-07-28 20:18:01.361802

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f929b673c253'
down_revision = 'b79a7e23434f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('users', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'last_seen')
    op.drop_column('users', 'about_me')
    # ### end Alembic commands ###
