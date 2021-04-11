"""add user_seen_poll table

Revision ID: c99e4797a586
Revises: 8b8f960f7288
Create Date: 2021-04-11 10:10:18.302770

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c99e4797a586'
down_revision = '8b8f960f7288'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_seen_poll',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('poll_id', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['poll_id'], ['poll.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_seen_poll_poll_id'), 'user_seen_poll', ['poll_id'], unique=False)
    op.create_index(op.f('ix_user_seen_poll_user_id'), 'user_seen_poll', ['user_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_seen_poll_user_id'), table_name='user_seen_poll')
    op.drop_index(op.f('ix_user_seen_poll_poll_id'), table_name='user_seen_poll')
    op.drop_table('user_seen_poll')
    # ### end Alembic commands ###