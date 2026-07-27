import mlflow
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

import numpy as np

app = FastAPI(title="Store Sales Inference Service")

RUN_ID = "6821e47f6a2847248329f7170d032ba1"
MODEL_URI = f"runs:/{RUN_ID}/catboost-model"
model = mlflow.pyfunc.load_model(MODEL_URI)


class UserActionItem(BaseModel):
    store_nbr: int
    onpromotion: int
    cluster: int
    dcoilwtico: float
    transactions_lag_16: float
    transactions_lag_30: float
    transactions_roll_mean_7: float
    transactions_roll_std_7: float
    dayofweek: int
    day: int
    month: int
    is_salary_day: int
    family: str
    city: str
    state: str
    type: str


@app.post("/predict")
def get_prediction(item: UserActionItem):
    input_data = pd.DataFrame([item.dict()])

    log_pred = model.predict(input_data)
    y_pred = np.expm1(log_pred)
    preds_real = np.clip(y_pred, 0, None)

    return {
        "status": "success",
        "prediction": float(preds_real[0])
    }

