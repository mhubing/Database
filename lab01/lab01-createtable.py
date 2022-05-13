import pymysql

# Connect to database
conn = pymysql.connect(	host='localhost',
						user='hb2002',
						password='2002',
						database='test')
# Create a cursor
c = conn.cursor()

# Create Table
# Book表
c.execute("Drop Table IF EXISTS Book")

sql="""CREATE TABLE IF NOT EXISTS Book(
ID char(8),
name varchar(10),
author varchar(10),
price float,
statue int DEFAULT 0,
Constraint PK_BID Primary Key(ID),
Constraint CK_BS Check (status IN (1, 0))
)"""
c.execute(sql)

# Reader 表
c.execute("Drop Table IF EXISTS Reader")

sql="""CREATE TABLE IF NOT EXISTS Reader(
ID char(8),
name varchar(10),
age int,
address varchar(20),
Constraint PK_RID Primary Key(ID)
)"""
c.execute(sql)

# Borrow表
c.execute("Drop Table IF EXISTS Borrow")

sql="""CREATE TABLE IF NOT EXISTS Borrow(
book_ID char(8),
Reader_ID char(8),
Borrow_Date DATE,
Return_Date DATE,
Constraint PK_B Primary Key(book_ID, Reader_ID),
Constraint FK_B1 Foreign Key(book_ID) References Book(ID),
Constraint FK_B2 Foreign Key(Reader_ID) References Reader(ID)
)"""
c.execute(sql)

print("finish")
conn.close()