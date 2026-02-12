import sqlite3
import pandas as pd

query = """
SELECT 
    month,
    day_of_week,
    is_holiday,
    is_promo,
    amount
FROM sales
WHERE date >= '2025-01-01'
"""

with sqlite3.connect("data.db") as connection:
    data = pd.read_sql(query, connection)

print(data.head(3))
print(data.shape)
data.to_csv("test.csv", index=False) # меняем train на test