import pandas as pd
from catboost import CatBoostRegressor
from sklearn.metrics import mean_absolute_percentage_error

train_data = pd.read_csv("train.csv")
test_data = pd.read_csv("test.csv")

X_train = train_data.drop(columns=['amount'])
y_train = train_data['amount']
X_test = test_data.drop(columns=['amount'])
y_test = test_data['amount']

model = CatBoostRegressor(cat_features=["store_type", "assortment"])
model.fit(X_train, y_train)

score = mean_absolute_percentage_error(y_test, model.predict(X_test))
print(f"Ошибка на тестовой выборке: {100 * score: .1f}%")

