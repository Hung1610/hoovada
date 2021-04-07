"""add id column for question_user_invite table

Revision ID: 99a4661da7dd
Revises: 4db95e3af3de
Create Date: 2021-04-06 11:32:18.257127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99a4661da7dd'
down_revision = '4db95e3af3de'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('question_user_invite', sa.Column('id', sa.Integer(), nullable=False, autoincrement=True, primary_key=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('question_user_invite', 'id')
    # ### end Alembic commands ###
