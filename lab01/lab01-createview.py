import pymysql

# Connect to database
conn = pymysql.connect(	host='localhost',
						user='hb2002',
						password='2002',
						database='test')
# Create a cursor
c = conn.cursor()

# Create View

c.execute("""DROP VIEW IF EXISTS br_view""")

sql="""
CREATE VIEW br_view (RID, Rname, BID, Bname, BorrowDate) AS
SELECT Reader.ID, Reader.name, Book.ID, Book.name, Borrow_Date
FROM Book, Reader, Borrow
WHERE Book.ID=book_ID and Reader.ID=Reader_ID;
"""

c.execute(sql)

print("Command executed successfully...")
conn.commit()
conn.close()