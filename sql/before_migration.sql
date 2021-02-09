SET GLOBAL log_bin_trust_function_creators = 1;


CREATE DATABASE IF NOT EXISTS hoovada CHARACTER SET utf8mb4;

USE hoovada;

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
IF length(b) > length(a) THEN
	RETURN ABS(((COMPARE_STRING(a, b) / length(b)) * 100) - 100);
ELSE
	RETURN ABS(((COMPARE_STRING(a, b) / length(a)) * 100) - 100);
END IF;
END$$
DELIMITER ;
