SELECT Book.name, Borrow.Borrow_Date
FROM Book, Reader, Borrow
WHERE Reader.name='Rose' and Book.ID=Borrow.book_ID and Reader.ID=Borrow.Reader_ID;