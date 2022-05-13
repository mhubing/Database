-- Create View
CREATE VIEW br_view (RID, Rname, BID, Bname, BorrowDate) AS
SELECT Reader.ID, Reader.name, Book.ID, Book.name, Borrow_Date
FROM Book, Reader, Borrow
WHERE Book.ID=book_ID and Reader.ID=Reader_ID;

-- 查询最近一年所有读者的读者号
SELECT br.RID
FROM br_view br
WHERE br.BorrowDate>DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
GROUP BY br.RID;

-- 查询最近一年所借阅的不同图书数
SELECT COUNT(DISTINCT BID) AS num
FROM br_view br
WHERE br.BorrowDate>DATE_SUB(CURDATE(), INTERVAL 1 YEAR);

-- 查询最近一年不同读者所借阅的图书数
SELECT br.RID, COUNT(*) AS Brnum
FROM br_view br
WHERE br.BorrowDate>DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
GROUP BY br.RID;
