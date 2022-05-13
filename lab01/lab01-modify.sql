delimiter //
DROP PROCEDURE IF EXISTS modify_bid;
CREATE PROCEDURE modify_bid(IN old_bid char(8), IN new_bid char(8), OUT state int)
BEGIN
	DECLARE s INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET s = 1;
	DECLARE CONTINUE HANDLER FOR 1451 SET s = 2;
	DECLARE CONTINUE HANDLER FOR 1452 SET s = 3;	
	START TRANSACTION;
	SET FOREIGN_KEY_CHECKS = 0;
	UPDATE Book SET ID=new_bid WHERE ID=old_bid;
	UPDATE Borrow SET book_ID=new_bid WHERE book_ID=old_bid;
	SET FOREIGN_KEY_CHECKS = 1;
	IF s=0 THEN
		SET state=0;
		COMMIT;
	ELSE
		CASE s
			WHEN 1 THEN SET state=1;
			WHEN 2 THEN SET state=2;
			WHEN 3 THEN SET state=3;
		END CASE;
		ROLLBACK;
	END IF;
END //
delimiter ;

CALL modify_bid('b1', 'b21', @state);
SELECT @state;
