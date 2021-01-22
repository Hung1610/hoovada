"""empty message

Revision ID: update_existing_null_1
Revises: f1526566268b
Create Date: 2021-01-11 09:59:41.434044

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'update_existing_null_1'
down_revision = 'f1526566268b'
branch_labels = None
depends_on = None


def upgrade():
    # update existing data for 
    # user table
    op.execute("UPDATE user SET topic_followed_count = 0 WHERE topic_followed_count is null")
    op.execute("UPDATE user SET topic_created_count = 0 WHERE topic_created_count is null")
    op.execute("UPDATE user SET article_aggregated_count = 0 WHERE article_aggregated_count is null")
    op.execute("UPDATE user SET answer_aggregated_count = 0 WHERE answer_aggregated_count is null")
    op.execute("UPDATE user SET question_aggregated_count = 0 WHERE question_aggregated_count is null")
    op.execute("UPDATE user SET post_count = 0 WHERE post_count is null")


def downgrade():
    pass
