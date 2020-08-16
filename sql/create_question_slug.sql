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