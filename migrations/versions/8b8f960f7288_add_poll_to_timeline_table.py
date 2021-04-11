"""add poll to timeline table

Revision ID: 8b8f960f7288
Revises: 79cf9c8fc152
Create Date: 2021-04-10 22:14:32.101374

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b8f960f7288'
down_revision = '79cf9c8fc152'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('timeline', sa.Column('poll_comment_id', sa.Integer(), nullable=True))
    op.add_column('timeline', sa.Column('poll_id', sa.Integer(), nullable=True))
    op.create_index(op.f('ix_timeline_poll_id'), 'timeline', ['poll_id'], unique=False)
    op.create_foreign_key(None, 'timeline', 'poll_comment', ['poll_comment_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'timeline', 'poll', ['poll_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'timeline', type_='foreignkey')
    op.drop_constraint(None, 'timeline', type_='foreignkey')
    op.drop_index(op.f('ix_timeline_poll_id'), table_name='timeline')
    op.drop_column('timeline', 'poll_id')
    op.drop_column('timeline', 'poll_comment_id')
    # ### end Alembic commands ###