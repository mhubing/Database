SELECT R1.name, R1.ID
FROM Reader R1
WHERE NOT EXISTS (
	SELECT * FROM Borrow B1 
	WHERE B1.Reader_ID=R1.ID and B1.book_ID IN(
		SELECT B2.book_ID FROM Borrow B2, Reader R2
		WHERE B2.Reader_ID=R2.ID and R2.name='李林'
	)
);