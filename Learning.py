import json

import mlflow
import mlflow.catboost
from catboost import CatBoostRegressor
import pandas as pd

X_train = pd.read_csv('model_input/X_train.csv')
y_train = pd.read_csv('model_input/y_train.csv')
X_val = pd.read_csv('model_input/X_val.csv')
y_val = pd.read_csv('model_input/y_val.csv')
with open('model_input/cat_features.json', 'r', encoding='utf-8') as file:
    cat_features = json.load(file)

mlflow.set_experiment("Store_Sales_Forecasting")
with mlflow.start_run(run_name="catboost_baseline"):

    params = {
        "iterations": 1500,
        "learning_rate": 0.01,
        "depth": 5,
        "eval_metric": "RMSE",
        "early_stopping_rounds": 100,
        "random_seed": 42
    }
    mlflow.log_params(params)
    mlflow.log_param("start_date", "2016-01-01")

    model = CatBoostRegressor(**params)

    model.fit(
        X_train, y_train,
        eval_set=[(X_val, y_val)],
        cat_features=cat_features,
        verbose=100
    )

    evals_result = model.get_evals_result()
    train_metrics = evals_result['learn']['RMSE']
    val_metrics = evals_result['validation']['RMSE']

    for i in range(len(train_metrics)):
        mlflow.log_metric("train_rmse", train_metrics[i], step=i)
        mlflow.log_metric("val_rmse", val_metrics[i], step=i)

    mlflow.log_metric("best_iteration", model.get_best_iteration())
    mlflow.log_metric("best_val_rmse", model.get_best_score()['validation']['RMSE'])

    mlflow.catboost.log_model(model, artifact_path="catboost-model")