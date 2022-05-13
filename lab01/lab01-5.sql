SELECT Book.ID,Book.name
FROM Book, Reader, Borrow
WHERE Reader.name='李林' and Return_Date IS NULL
		and Book.ID=book_ID and Reader.ID=Reader_ID;