"""empty message

Revision ID: c73b6453113d
Revises: 64e8f8005ff1
Create Date: 2017-01-18 13:38:12.130954

"""

# revision identifiers, used by Alembic.
revision = 'c73b6453113d'
down_revision = '64e8f8005ff1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'phone_number')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('phone_number', sa.INTEGER(), autoincrement=False, nullable=True))
    ### end Alembic commands ###
