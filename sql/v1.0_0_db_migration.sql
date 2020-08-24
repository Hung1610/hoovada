ALTER DATABASE hoovada CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE alembic_version CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.alembic_version CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE answer CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.answer CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE article CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.article CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE article_comment CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.article_comment CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE article_favorite CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.article_favorite CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE article_report CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.article_report CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE article_share CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.article_share CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE article_vote CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.article_vote CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE blacklist_tokens CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.blacklist_tokens CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE comment CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.comment CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE favorite CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.favorite CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE question CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.question CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE question_topic CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.question_topic CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE recovery_user CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.recovery_user CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE report CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.report CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE reputation CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.reputation CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE share CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.share CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE signup_user CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.signup_user CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE social_account CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.social_account CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE topic CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.topic CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE topic_article CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.topic_article CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE user CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.user CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE user_employment CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.user_employment CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE user_topic CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.user_topic CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  
ALTER TABLE vote CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  ALTER TABLE hoovada.vote CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;  

DELETE FROM `user_topic` WHERE `topic_id` = (SELECT `id` FROM `topic` WHERE `name` = "Sản phẩm của yahoo");
DELETE FROM `question_topic` WHERE `topic_id` = (SELECT `id` FROM `topic` WHERE `name` = "Sản phẩm của yahoo");
DELETE FROM `topic` WHERE `name` = "Sản phẩm của yahoo";
ALTER TABLE `user` CHANGE `id` `id` INT(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `topic` CHANGE `id` `id` INT(11) NOT NULL AUTO_INCREMENT;
DELETE n1 FROM user n1, user n2 WHERE n1.id > n2.id AND n1.display_name = n2.display_name;
update user set profile_pic_url=Null;

ALTER TABLE `question` ADD `slug` VARCHAR(255) NOT NULL AFTER `favorite_count`;

ALTER
 ALGORITHM = UNDEFINED
DEFINER=`dev`@`%` 
 SQL SECURITY DEFINER
 VIEW `topic_question`
 AS SELECT
    `hoovada`.`topic`.`id` AS `topic_id`,
    `hoovada`.`topic`.`name` AS `topic_name`,
    `hoovada`.`question`.`id` AS `id`,
    `hoovada`.`question`.`title` AS `title`,
    `hoovada`.`question`.`user_id` AS `user_id`,
    `hoovada`.`question`.`fixed_topic_id` AS `fixed_topic_id`,
    `hoovada`.`question`.`fixed_topic_name` AS `fixed_topic_name`,
    `hoovada`.`question`.`question` AS `question`,
    `hoovada`.`question`.`markdown` AS `markdown`,
    `hoovada`.`question`.`html` AS `html`,
    `hoovada`.`question`.`created_date` AS `created_date`,
    `hoovada`.`question`.`updated_date` AS `updated_date`,
    `hoovada`.`question`.`views_count` AS `views_count`,
    `hoovada`.`question`.`last_activity` AS `last_activity`,
    `hoovada`.`question`.`answers_count` AS `answers_count`,
    `hoovada`.`question`.`accepted_answer_id` AS `accepted_answer_id`,
    `hoovada`.`question`.`anonymous` AS `anonymous`,
    `hoovada`.`question`.`user_hidden` AS `user_hidden`,
    `hoovada`.`question`.`image_ids` AS `image_ids`,
    `hoovada`.`question`.`upvote_count` AS `upvote_count`,
    `hoovada`.`question`.`downvote_count` AS `downvote_count`,
    `hoovada`.`question`.`share_count` AS `share_count`,
    `hoovada`.`question`.`favorite_count` AS `favorite_count`,
    `hoovada`.`question`.`slug` AS `slug`
FROM
    (
        `hoovada`.`question`
    JOIN(
            `hoovada`.`question_topic`
        JOIN `hoovada`.`topic` ON
            (
                (
                    `hoovada`.`question_topic`.`topic_id` = `hoovada`.`topic`.`id`
                )
            )
        )
    ON
        (
            (
                `hoovada`.`question_topic`.`question_id` = `hoovada`.`question`.`id`
            )
        )
    )
