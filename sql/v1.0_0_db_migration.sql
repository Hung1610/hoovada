ALTER TABLE share change shared_date created_date datetime;
ALTER TABLE user ADD COLUMN user_report_count int(11) default 0;
ALTER TABLE user ADD COLUMN user_reported_count int(11) default 0;
ALTER TABLE user ADD COLUMN question_report_count int(11) default 0;
ALTER TABLE user ADD COLUMN question_reported_count int(11) default 0;
ALTER TABLE user ADD COLUMN answer_report_count int(11) default 0;
ALTER TABLE user ADD COLUMN answer_reported_count int(11) default 0;
ALTER TABLE user ADD COLUMN question_upvote_count int(11) default 0;
ALTER TABLE user ADD COLUMN question_upvoted_count int(11) default 0;
ALTER TABLE user ADD COLUMN question_downvote_count int(11) default 0;
ALTER TABLE user ADD COLUMN question_downvoted_count int(11) default 0;

CREATE TABLE `social_account` (
  `id` int(11) NOT NULL,
  `provider` varchar(30) COLLATE utf8_unicode_ci NOT NULL,
  `uid` varchar(200) COLLATE utf8_unicode_ci NOT NULL,
  `last_login` datetime(6) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `extra_data` longtext COLLATE utf8_unicode_ci NOT NULL,
  `user_id` int(11) NOT NULL
);

ALTER TABLE `user` ADD COLUMN `phone_number` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL;
ALTER TABLE `user` ADD COLUMN `verification_sms_time` datetime DEFAULT NULL;

ALTER TABLE `user`
  ADD UNIQUE KEY `display_name` (`display_name`),
  ADD UNIQUE KEY `phone_number` (`phone_number`);

ALTER TABLE `social_account` ADD PRIMARY KEY (`id`);
ALTER TABLE `social_account` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
ALTER TABLE `user` MODIFY `email` varchar(255) COLLATE utf8_general_ci NULL;


DELETE FROM `user_topic` WHERE `topic_id` = (SELECT `id` FROM `topic` WHERE `name` = "Sản phẩm của yahoo");
DELETE FROM `question_topic` WHERE `topic_id` = (SELECT `id` FROM `topic` WHERE `name` = "Sản phẩm của yahoo");
DELETE FROM `topic` WHERE `name` = "Sản phẩm của yahoo";

CREATE TABLE `user_employment` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `position` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `company` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `start_year` year(4) DEFAULT NULL,
  `end_year` year(4) DEFAULT NULL,
  `is_currently_work` tinyint(1) DEFAULT NULL,
  `is_default` tinyint(1) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL
);

ALTER TABLE `user_employment` ADD PRIMARY KEY (`id`);
ALTER TABLE `user_employment` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE user
    DROP COLUMN city, 
    DROP COLUMN country, 
    DROP COLUMN job_role, 
    DROP COLUMN company, 
    DROP COLUMN website_url;

ALTER TABLE user MODIFY COLUMN id Integer(11);
ALTER TABLE topic MODIFY COLUMN id Integer(11);
DELETE n1 FROM user n1, user n2 WHERE n1.id > n2.id AND n1.display_name = n2.display_name;
RENAME TABLE topic_question to topic_question_view;

