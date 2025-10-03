from fastapi import APIRouter
from app.schemas.predict_schemas import LoanApplication
import pandas as pd
import joblib
import os

router = APIRouter()

MODEL_PATH = os.path.join("model", "loan_model_pipeline.joblib")
model_pipeline = joblib.load(MODEL_PATH)

@router.post("/predict")
def predict_loan(application: LoanApplication):
    input_data = pd.DataFrame([application.dict()])
    prediction = model_pipeline.predict(input_data)[0]
    probability = model_pipeline.predict_proba(input_data)[0][1]

    return {
        "prediction": "Approved" if prediction == 1 else "Rejected",
        "probability": round(probability * 100, 2)
    }
