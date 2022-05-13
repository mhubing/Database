SELECT Reader.name
FROM Reader
WHERE Reader.ID NOT IN (SELECT Reader_ID From Borrow);