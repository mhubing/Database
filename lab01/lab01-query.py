import pymysql

# Connect to database
conn = pymysql.connect(	host='localhost',
						user='hb2002',
						password='2002',
						database='test')
# Create a cursor
c = conn.cursor()

# Query the Database
sql="""
SELECT br.RID, COUNT(*) AS Brnum
FROM br_view br
WHERE br.BorrowDate>DATE_SUB(CURDATE(), INTERVAL 1 YEAR)
GROUP BY br.RID;
"""


c.execute(sql)

items = c.fetchall()
for item in items:
	print(item)

print("\nCommand executed successfully...")

# Commit command
conn.commit()

# Close connection
conn.close()