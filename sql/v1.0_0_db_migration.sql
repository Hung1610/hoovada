
DELETE FROM `user_topic` WHERE `topic_id` = (SELECT `id` FROM `topic` WHERE `name` = "Sản phẩm của yahoo");
DELETE FROM `question_topic` WHERE `topic_id` = (SELECT `id` FROM `topic` WHERE `name` = "Sản phẩm của yahoo");
DELETE FROM `topic` WHERE `name` = "Sản phẩm của yahoo";
ALTER TABLE `user` CHANGE `id` `id` INT(11) NOT NULL AUTO_INCREMENT;
ALTER TABLE `topic` CHANGE `id` `id` INT(11) NOT NULL AUTO_INCREMENT;
DELETE n1 FROM user n1, user n2 WHERE n1.id > n2.id AND n1.display_name = n2.display_name;
update user set profile_pic_url=Null;

