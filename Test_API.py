import requests

url = "http://127.0.0.1:8000/predict"

payload = {
  "store_nbr": 54,
  "onpromotion": 0,
  "cluster": 3,
  "dcoilwtico": 47.57,
  "transactions_lag_16": 802.0,
  "transactions_lag_30": 818.0,
  "transactions_roll_mean_7": 802.0,
  "transactions_roll_std_7": 0,
  "dayofweek": 1,
  "day": 15,
  "month": 8,
  "is_salary_day": 1,
  "family": "POULTRY",
  "city": "El Carmen",
  "state": "Manabi",
  "type": "C"
}

response = requests.post(url, json=payload)

if response.status_code == 200:
    print("Ответ сервера успешен!")
    print("Результат прогноза:", response.json())
else:
    print(f"Ошибка! Статус-код: {response.status_code}")
    print(response.text)