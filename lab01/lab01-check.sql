-- 检查每本图书的status是否正确，并返回status不正确的图书数
delimiter //
DROP PROCEDURE IF EXISTS check_status;
CREATE PROCEDURE check_status(OUT state int, OUT num int)
BEGIN
	DECLARE s INT DEFAULT 0;
	DECLARE n INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET s = 1;	
	START TRANSACTION;
	SELECT COUNT(*) AS count FROM(
		SELECT DISTINCT ID FROM Book
		WHERE (Book.status=0 and EXISTS(SELECT * FROM  Borrow WHERE Borrow.book_ID=Book.ID and Return_Date IS NULL))
		or (Book.status=1 and NOT EXISTS(SELECT * FROM  Borrow WHERE Borrow.book_ID=Book.ID and Return_Date IS NULL))
		GROUP BY ID
	) a INTO n;
	
	SET num=n;

	IF s=0 THEN
		SET state=0;
		COMMIT;
	ELSE
		CASE s
			WHEN 1 THEN SET state=1;
			ELSE SET state=2;
		END CASE;
		ROLLBACK;
	END IF;
END //
delimiter ;

CALL check_status(@state, @num);
SELECT @state, @num;