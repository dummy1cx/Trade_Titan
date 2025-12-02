from fastapi import APIRouter, HTTPException
from app.schemas.read_schemas import InsuranceInput, InsuranceResponse
import joblib
import pandas as pd

router = APIRouter(prefix="/predict", tags=["Insurance Predictor"])

model_path = "model/xgb_insurance_model.joblib"
scaler_path = "model/insurance_preprocessor.joblib"

insurance_model = joblib.load(model_path)
insurance_scaler = joblib.load(scaler_path)

@router.post("/insurance", response_model=InsuranceResponse, summary="Predict insurance premium cost")
def predict_insurance(payload: InsuranceInput):
    """
    Predict the insurance premium for a person based on the given features.
    """

    try:
        # Data frame from the input columns
        df = pd.DataFrame([{
            "age": payload.age,
            "sex": payload.sex,
            "bmi": payload.bmi,
            "children": payload.children,
            "smoker": payload.smoker,
            "region": payload.region
        }])

        # Loading the pre processr pipeline
        try:
            X_scaled = insurance_scaler.transform(df)
        except Exception as e:
            print("Preprocessor skipped:", e)
            X_scaled = df

        # Prediction from the model
        prediction = insurance_model.predict(X_scaled)[0]

        return {
            "predicted_premium": float(prediction),
            "model_version": "XGB_Insurance_v1"
        }

    except Exception as e:
        print("Error during insurance prediction:", e)
        raise HTTPException(status_code=500, detail=str(e))
