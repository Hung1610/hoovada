"""empty message

Revision ID: update_unique_answer
Revises: 962d952b1c63
Create Date: 2021-01-11 09:59:41.434044

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = 'update_unique_answer'
down_revision = '962d952b1c63'
branch_labels = None
depends_on = None



def upgrade():
    # update existing data for answer table
    op.execute("CREATE TEMPORARY TABLE IF NOT EXISTS answer2 engine=memory \
        SELECT MIN(id) as id, user_id, question_id \
        FROM answer \
        GROUP BY user_id, question_id")

    op.execute("DELETE a FROM answer as a \
        LEFT  JOIN ( \
        SELECT * from answer2 \
        ) as b ON \
        b.id = a.id \
        WHERE \
        b.id IS NULL")


def downgrade():
    pass
