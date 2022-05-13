SELECT Reader.ID, Reader.name, Reader.age, COUNT(*) AS bnum
FROM Reader, Borrow
WHERE YEAR(Borrow_date)=2021 and Reader.ID=Reader_ID
GROUP BY Reader.ID
ORDER BY bnum DESC
LIMIT 20;