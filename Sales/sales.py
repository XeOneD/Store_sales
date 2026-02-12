import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(cursor.fetchall())

cursor.execute('SELECT * FROM sales LIMIT 0')
titles_sales = [desc[0] for desc in cursor.description]
# title2 = list(map(lambda x: x[0], cursor.description))
print(titles_sales)

cursor.execute('SELECT * FROM sales LIMIT 5')
sales = cursor.fetchall()
for sale in sales:
    print(sale)

cursor.execute('SELECT * FROM stores LIMIT 0')
titles_stores = list(map(lambda x: x[0], cursor.description))
print(titles_stores)

cursor.execute('SELECT * FROM stores LIMIT 5')
stores = cursor.fetchall()
for store in stores:
    print(store)



amount_of_rows_sales = cursor.execute('SELECT COUNT(*) FROM sales;')
print(amount_of_rows_sales.fetchall()[0][0])

amount_of_rows_stores = cursor.execute('SELECT COUNT(*) FROM stores')
print(amount_of_rows_stores.fetchall()[0][0])

min_max_date = cursor.execute('SELECT MIN(date), MAX(date) FROM sales')
print(min_max_date.fetchall())

min_avg_max_amount = cursor.execute('SELECT MIN(amount), AVG(amount), MAX(amount) FROM sales')
print(min_avg_max_amount.fetchall())

everyday_avg = cursor.execute('SELECT day_of_week, AVG(amount) FROM sales GROUP BY day_of_week')
for sale in everyday_avg:
    print(sale)

connection.close()