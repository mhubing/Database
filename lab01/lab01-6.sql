SELECT Reader.name
FROM Reader, Borrow
WHERE Reader.ID=Reader_ID
GROUP BY Reader.ID
HAVING count(*)>3;