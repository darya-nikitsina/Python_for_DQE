import sqlite3

db_name = 'NewsFeedDatabase.db'

connection = sqlite3.connect(db_name)
cursor = connection.cursor()

cursor.execute('''
    SELECT *
    FROM News''')

result = cursor.fetchall()

print(result)