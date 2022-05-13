-- 当一本书被借出时（INSERT），将Book表中相应图书的status修改为1
delimiter //
DROP TRIGGER IF EXISTS set_status;
CREATE TRIGGER set_status
AFTER INSERT ON Borrow For Each Row
BEGIN
	UPDATE Book SET status=1
	WHERE Book.ID=new.book_ID and new.Return_Date IS NULL;
END //
delimiter ;


-- 当一本书被归还时（UPDATE），将Book表中相应图书的status修改为0
delimiter //
DROP TRIGGER IF EXISTS unset_status;
CREATE TRIGGER unset_status
AFTER UPDATE ON Borrow For Each Row
BEGIN
	UPDATE Book SET status=0
	WHERE Book.ID=new.book_ID and new.Return_Date IS NOT NULL;
END //
delimiter ;
