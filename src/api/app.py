from fastapi import FastAPI
import xgboost as xgb
import pandas as pd

app = FastAPI()

# Load trained model
model = xgb.XGBClassifier()
model.load_model("models/financial_risk_model.json")

@app.post("/predict/")
def predict(data: dict):
    df = pd.DataFrame([data])
    prediction = model.predict(df)
    return {"risk_level": int(prediction[0])}
