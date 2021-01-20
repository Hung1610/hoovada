"""empty message

Revision ID: edfa2573c56e
Revises: update_existing_null_1
Create Date: 2021-01-20 22:36:03.786272

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'edfa2573c56e'
down_revision = 'update_existing_null_1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('answer', 'allow_comments',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('answer', 'allow_improvement',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('answer', 'is_anonymous',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=False)
    op.alter_column('answer', 'is_deleted',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=False)
    op.alter_column('article', 'is_anonymous',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=False)
    op.alter_column('article', 'is_deleted',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=False)
    op.alter_column('article', 'is_draft',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=True)
    op.alter_column('post', 'allow_favorite',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('post', 'is_deleted',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=False)
    op.alter_column('post', 'is_draft',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=True)
    op.alter_column('question', 'allow_audio_answer',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=True)
    op.alter_column('question', 'allow_comments',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('question', 'allow_video_answer',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=True)
    op.alter_column('question', 'is_anonymous',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=False)
    op.alter_column('question', 'is_deleted',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=False)
    op.alter_column('question', 'is_private',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=True)
    op.alter_column('question_proposal', 'allow_audio_answer',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=True)
    op.alter_column('question_proposal', 'allow_comments',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('question_proposal', 'allow_video_answer',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=True)
    op.alter_column('question_proposal', 'is_anonymous',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=False)
    op.alter_column('question_proposal', 'is_approved',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=True)
    op.alter_column('question_proposal', 'is_deleted',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=False)
    op.alter_column('question_proposal', 'is_parma_delete',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=True)
    op.alter_column('question_proposal', 'is_private',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=True)
    op.alter_column('topic', 'allow_follow',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('topic', 'is_nsfw',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=True)
    op.alter_column('user', 'admin_interaction_email_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('user', 'admin_interaction_notify_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('user', 'answer_aggregated_count',
               existing_type=mysql.INTEGER(display_width=11),
               server_default='0',
               nullable=False)
    op.alter_column('user', 'article_aggregated_count',
               existing_type=mysql.INTEGER(display_width=11),
               server_default='0',
               nullable=False)
    op.alter_column('user', 'follow_email_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('user', 'follow_notify_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('user', 'followed_new_publication_email_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('user', 'followed_new_publication_notify_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('user', 'friend_request_email_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('user', 'friend_request_notify_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('user', 'is_birthday_hidden',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=True)
    op.alter_column('user', 'is_deactivated',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=True)
    op.alter_column('user', 'is_private',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=True)
    op.alter_column('user', 'my_question_email_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('user', 'my_question_notify_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('user', 'new_answer_comment_email_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('user', 'new_answer_comment_notify_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('user', 'new_answer_email_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('user', 'new_answer_notify_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('user', 'new_article_comment_email_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('user', 'new_article_comment_notify_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('user', 'new_question_comment_email_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('user', 'new_question_comment_notify_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('user', 'post_count',
               existing_type=mysql.INTEGER(display_width=11),
               server_default='0',
               nullable=False)
    op.alter_column('user', 'question_aggregated_count',
               existing_type=mysql.INTEGER(display_width=11),
               server_default='0',
               nullable=False)
    op.alter_column('user', 'question_invite_email_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('user', 'question_invite_notify_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('true'),
               existing_nullable=True)
    op.alter_column('user', 'show_nsfw',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text('false'),
               existing_nullable=True)
    op.alter_column('user', 'topic_created_count',
               existing_type=mysql.INTEGER(display_width=11),
               server_default='0',
               nullable=False)
    op.alter_column('user', 'topic_followed_count',
               existing_type=mysql.INTEGER(display_width=11),
               server_default='0',
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'topic_followed_count',
               existing_type=mysql.INTEGER(display_width=11),
               server_default=None,
               nullable=True)
    op.alter_column('user', 'topic_created_count',
               existing_type=mysql.INTEGER(display_width=11),
               server_default=None,
               nullable=True)
    op.alter_column('user', 'show_nsfw',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=True)
    op.alter_column('user', 'question_invite_notify_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('user', 'question_invite_email_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('user', 'question_aggregated_count',
               existing_type=mysql.INTEGER(display_width=11),
               server_default=None,
               nullable=True)
    op.alter_column('user', 'post_count',
               existing_type=mysql.INTEGER(display_width=11),
               server_default=None,
               nullable=True)
    op.alter_column('user', 'new_question_comment_notify_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('user', 'new_question_comment_email_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('user', 'new_article_comment_notify_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('user', 'new_article_comment_email_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('user', 'new_answer_notify_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('user', 'new_answer_email_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('user', 'new_answer_comment_notify_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('user', 'new_answer_comment_email_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('user', 'my_question_notify_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('user', 'my_question_email_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('user', 'is_private',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=True)
    op.alter_column('user', 'is_deactivated',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=True)
    op.alter_column('user', 'is_birthday_hidden',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=True)
    op.alter_column('user', 'friend_request_notify_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('user', 'friend_request_email_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('user', 'followed_new_publication_notify_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('user', 'followed_new_publication_email_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('user', 'follow_notify_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('user', 'follow_email_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('user', 'article_aggregated_count',
               existing_type=mysql.INTEGER(display_width=11),
               server_default=None,
               nullable=True)
    op.alter_column('user', 'answer_aggregated_count',
               existing_type=mysql.INTEGER(display_width=11),
               server_default=None,
               nullable=True)
    op.alter_column('user', 'admin_interaction_notify_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('user', 'admin_interaction_email_settings',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('topic', 'is_nsfw',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=True)
    op.alter_column('topic', 'allow_follow',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('question_proposal', 'is_private',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=True)
    op.alter_column('question_proposal', 'is_parma_delete',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=True)
    op.alter_column('question_proposal', 'is_deleted',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=False)
    op.alter_column('question_proposal', 'is_approved',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=True)
    op.alter_column('question_proposal', 'is_anonymous',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=False)
    op.alter_column('question_proposal', 'allow_video_answer',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=True)
    op.alter_column('question_proposal', 'allow_comments',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('question_proposal', 'allow_audio_answer',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=True)
    op.alter_column('question', 'is_private',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=True)
    op.alter_column('question', 'is_deleted',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=False)
    op.alter_column('question', 'is_anonymous',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=False)
    op.alter_column('question', 'allow_video_answer',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=True)
    op.alter_column('question', 'allow_comments',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('question', 'allow_audio_answer',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=True)
    op.alter_column('post', 'is_draft',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=True)
    op.alter_column('post', 'is_deleted',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=False)
    op.alter_column('post', 'allow_favorite',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('article', 'is_draft',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=True)
    op.alter_column('article', 'is_deleted',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=False)
    op.alter_column('article', 'is_anonymous',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=False)
    op.alter_column('answer', 'is_deleted',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=False)
    op.alter_column('answer', 'is_anonymous',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'0'"),
               existing_nullable=False)
    op.alter_column('answer', 'allow_improvement',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    op.alter_column('answer', 'allow_comments',
               existing_type=mysql.TINYINT(display_width=1),
               server_default=sa.text("'1'"),
               existing_nullable=True)
    # ### end Alembic commands ###
