"""empty message

Revision ID: update_existing_null
Revises: 71f6c84e34d1
Create Date: 2021-01-11 09:59:41.434044

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'update_existing_null'
down_revision = '71f6c84e34d1'
branch_labels = None
depends_on = None


def upgrade():
    # update existing data for 
    # question table
    op.execute("UPDATE question SET answers_count = 0 WHERE answers_count is null")
    op.execute("UPDATE question SET upvote_count = 0 WHERE upvote_count is null")
    op.execute("UPDATE question SET downvote_count = 0 WHERE downvote_count is null")
    op.execute("UPDATE question SET share_count = 0 WHERE share_count is null")
    op.execute("UPDATE question SET favorite_count = 0 WHERE favorite_count is null")
    op.execute("UPDATE question SET comment_count = 0 WHERE comment_count is null")
    # article table
    op.execute("UPDATE article SET upvote_count = 0 WHERE upvote_count is null")
    op.execute("UPDATE article SET downvote_count = 0 WHERE downvote_count is null")
    op.execute("UPDATE article SET share_count = 0 WHERE share_count is null")
    op.execute("UPDATE article SET favorite_count = 0 WHERE favorite_count is null")
    op.execute("UPDATE article SET comment_count = 0 WHERE comment_count is null")
    # answer table
    op.execute("UPDATE answer SET upvote_count = 0 WHERE upvote_count is null")
    op.execute("UPDATE answer SET downvote_count = 0 WHERE downvote_count is null")
    op.execute("UPDATE answer SET share_count = 0 WHERE share_count is null")
    op.execute("UPDATE answer SET favorite_count = 0 WHERE favorite_count is null")
    op.execute("UPDATE answer SET comment_count = 0 WHERE comment_count is null")


def downgrade():
    pass
