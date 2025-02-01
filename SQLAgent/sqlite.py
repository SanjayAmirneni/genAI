import sqlite3

## Connect to sqlite database
connection = sqlite3.connect('student.db')

## create a cursor object
cursor = connection.cursor()


## create the table
table_info = """
CREATE TABLE STUDENT (NAME VARCHAR9(25), CLASS VARCHAR(10), SECTION VARCHAR(10), MARKS INT);"""

cursor.execute(table_info)

## Insert some more records
cursor.execute('''Insert Into STUDENT values('Krish','Data Science','A',90)''')
cursor.execute('''Insert Into STUDENT values('John','Data Science','B',100)''')
cursor.execute('''Insert Into STUDENT values('Mukesh','Data Science','A',86)''')
cursor.execute('''Insert Into STUDENT values('Jacob','DEVOPS','A',50)''')
cursor.execute('''Insert Into STUDENT values('Dipesh','DEVOPS','A',35)''')

## Display the records
data=cursor.execute('''SELECT * FROM STUDENT''')
for row in data:
    print(row)

## commit the transaction
connection.commit()
connection.close()