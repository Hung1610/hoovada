USE hoovada;

UPDATE user SET
    new_answer_notify_settings = 0,
    new_answer_email_settings = 0,
    my_question_notify_settings = 0,
    my_question_email_settings = 0,
    new_question_comment_notify_settings = 0,
    new_question_comment_email_settings = 0,
    new_answer_comment_notify_settings = 0,
    new_answer_comment_email_settings = 0,
    new_article_comment_notify_settings = 0,
    new_article_comment_email_settings = 0,
    question_invite_notify_settings = 0,
    question_invite_email_settings = 0,
    follow_notify_settings = 0,
    follow_email_settings = 0,
    followed_new_publication_notify_settings = 0,
    followed_new_publication_email_settings = 0;
