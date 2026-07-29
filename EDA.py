import json

import pandas as pd
import numpy as np

holiday_events = pd.read_csv('data/holidays_events.csv', parse_dates=['date'])
oil = pd.read_csv('data/oil.csv', parse_dates=['date'])
stores = pd.read_csv('data/stores.csv')
transactions = pd.read_csv('data/transactions.csv', parse_dates=['date'])
train_data = pd.read_csv('data/train.csv', parse_dates=['date'])
test_data = pd.read_csv('data/test.csv', parse_dates=['date'])

oil['dcoilwtico'] = oil['dcoilwtico'].ffill().bfill()

train_data = pd.merge(train_data, stores, on='store_nbr', how='left')
test_data = pd.merge(test_data, stores, on='store_nbr', how='left')
train_data = pd.merge(train_data, oil, on='date', how='left')
test_data = pd.merge(test_data, oil, on='date', how='left')

train_data_idx = len(train_data)

df = pd.concat([train_data, test_data], axis=0, ignore_index=True)
df = df.sort_values(['date', 'store_nbr', 'family']).reset_index(drop=True)
df = pd.merge(df, transactions, on=['date', 'store_nbr'], how='left')

df['transactions'] = df['transactions'].fillna(0)
df['transactions_lag_16'] = df.groupby('store_nbr')['transactions'].transform(lambda x: x.shift(16))
df['transactions_lag_30'] = df.groupby('store_nbr')['transactions'].transform(lambda x: x.shift(30))
df['transactions_roll_mean_7'] = df.groupby('store_nbr')['transactions_lag_16'].transform(lambda x: x.rolling(7).mean())
df['transactions_roll_std_7'] = df.groupby('store_nbr')['transactions_lag_16'].transform(lambda x: x.rolling(7).std())
df['transactions_lag_16'] = df['transactions_lag_16'].fillna(df['transactions_lag_16'].mean())
df['transactions_lag_30'] = df['transactions_lag_30'].fillna(df['transactions_lag_30'].mean())
df['transactions_roll_mean_7'] = df['transactions_roll_mean_7'].fillna(df['transactions_roll_mean_7'].mean())
df['transactions_roll_std_7'] = df['transactions_roll_std_7'].fillna(df['transactions_roll_std_7'].mean())
df['dcoilwtico'] = df['dcoilwtico'].fillna(df['dcoilwtico'].mean())
df['dayofweek'] = df['date'].dt.dayofweek
df['day'] = df['date'].dt.day
df['month'] = df['date'].dt.month
df['is_salary_day'] = df['day'].isin([15, 16, 30, 31]).astype(int)
df = df.drop(columns=['transactions'])

train_final = df.iloc[:train_data_idx].copy()
test_final = df.iloc[train_data_idx:].copy()

train_final['target_log'] = np.log1p(train_final['sales'])

start_date = '2016-01-01'
train_final = train_final[train_final['date'] >= start_date]
split_date = '2017-07-31'
train_data = train_final[train_final['date'] < split_date]
val_data = train_final[train_final['date'] >= split_date]

features = [
    'store_nbr', 'onpromotion', 'cluster', 'dcoilwtico',
    'transactions_lag_16', 'transactions_lag_30',
    'transactions_roll_mean_7', 'transactions_roll_std_7',
    'dayofweek', 'day', 'month', 'is_salary_day', 'family',
    'city', 'state', 'type'
]
cat_features = ['family', 'city', 'state', 'type']

with open('model_input/cat_features.json', 'w', encoding='utf-8') as file:
    json.dump(cat_features, file, indent=4)

train_data[features].to_csv('model_input/X_train.csv', index=False)
train_data['target_log'].to_csv('model_input/y_train.csv', index=False)
val_data[features].to_csv('model_input/X_val.csv', index=False)
val_data['target_log'].to_csv('model_input/y_val.csv', index=False)