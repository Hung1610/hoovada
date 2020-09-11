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

SET GLOBAL log_bin_trust_function_creators = 1;
DELIMITER $$
CREATE DEFINER=`root`@`localhost` FUNCTION `COMPARE_STRING`( s1 text, s2 text) RETURNS int(11)
    DETERMINISTIC
BEGIN 
    DECLARE s1_len, s2_len, i, j, c, c_temp, cost INT; 
    DECLARE s1_char CHAR; 
    DECLARE cv0, cv1 text; 
    SET s1_len = CHAR_LENGTH(s1), s2_len = CHAR_LENGTH(s2), cv1 = 0x00, j = 1, i = 1, c = 0; 
    IF s1 = s2 THEN 
      RETURN 0;     
    ELSEIF s1_len = 0 THEN 
      RETURN s2_len; 
    ELSEIF s2_len = 0 THEN 
      RETURN s1_len; 
    ELSE 
      WHILE j <= s2_len DO 
        SET cv1 = CONCAT(cv1, UNHEX(HEX(j))), j = j + 1; 
      END WHILE; 
      WHILE i <= s1_len DO 
        SET s1_char = SUBSTRING(s1, i, 1), c = i, cv0 = UNHEX(HEX(i)), j = 1; 
        WHILE j <= s2_len DO 
          SET c = c + 1; 
          IF s1_char = SUBSTRING(s2, j, 1) THEN  
            SET cost = 0; ELSE SET cost = 1; 
          END IF; 
          SET c_temp = CONV(HEX(SUBSTRING(cv1, j, 1)), 16, 10) + cost; 
          IF c > c_temp THEN SET c = c_temp; END IF; 
            SET c_temp = CONV(HEX(SUBSTRING(cv1, j+1, 1)), 16, 10) + 1; 
            IF c > c_temp THEN  
              SET c = c_temp;  
            END IF; 
            SET cv0 = CONCAT(cv0, UNHEX(HEX(c))), j = j + 1; 
        END WHILE; 
        SET cv1 = cv0, i = i + 1; 
      END WHILE; 
    END IF; 
    RETURN c; 
  END$$
DELIMITER ;

DELIMITER $$
CREATE DEFINER=`root`@`localhost` FUNCTION `SIMILARITY_STRING`(a text, b text) RETURNS double
BEGIN
RETURN ABS(((COMPARE_STRING(a, b) / length(b)) * 100) - 100);
END$$
DELIMITER ;

ALTER TABLE `hoovada`.`question` CHANGE COLUMN `id` `id` INT(10) NOT NULL AUTO_INCREMENT;
ALTER TABLE `hoovada`.`answer` CHANGE `id` `id` INT(10) NOT NULL AUTO_INCREMENT;
ALTER TABLE `hoovada`.`comment` CHANGE `id` `id` INT(10) NOT NULL AUTO_INCREMENT;
UPDATE question SET is_private = False;
SET SQL_SAFE_UPDATES = 0;
DELETE FROM question WHERE user_id NOT IN (SELECT user.id FROM user);
SET SQL_SAFE_UPDATES = 0;
DELETE FROM question_topic WHERE question_id NOT IN (SELECT question .id FROM question);
SET SQL_SAFE_UPDATES = 0;
DELETE FROM answer WHERE user_id NOT IN (SELECT user.id FROM user);
SET SQL_SAFE_UPDATES = 0;
DELETE FROM answer WHERE question_id NOT IN (SELECT question.id FROM question);
SET SQL_SAFE_UPDATES = 0;
DELETE FROM user_topic WHERE fixed_topic_id NOT IN (SELECT topic.id FROM topic);






