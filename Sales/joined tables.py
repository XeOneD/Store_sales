import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

cursor.execute("SELECT date, amount, store_type FROM sales JOIN stores USING(store_id) LIMIT 5")
print(cursor.fetchall())

cursor.execute("SELECT store_type, AVG(amount) FROM sales JOIN stores USING(store_id) GROUP BY store_type")
print(cursor.fetchall())

cursor.execute("SELECT assortment, AVG(amount) FROM sales JOIN stores USING(store_id) GROUP BY assortment")
print(cursor.fetchall())