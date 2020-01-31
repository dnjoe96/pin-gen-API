"""change

Revision ID: 2d0e8f916fb6
Revises: 
Create Date: 2020-01-30 20:54:51.777727

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d0e8f916fb6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Pin',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('s_n', sa.Integer(), nullable=False),
    sa.Column('pin', sa.String(length=140), nullable=False),
    sa.Column('request_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('pin'),
    sa.UniqueConstraint('s_n')
    )
    op.create_index(op.f('ix_Pin_request_time'), 'Pin', ['request_time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_Pin_request_time'), table_name='Pin')
    op.drop_table('Pin')
    # ### end Alembic commands ###
