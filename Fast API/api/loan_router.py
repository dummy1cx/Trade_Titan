from fastapi import APIRouter
import joblib
import pandas as pd
from app.schemas.read_schemas import LoanApplication, LoanResponse

router = APIRouter(prefix="/predict", tags=["Loan Predictor"])

# Load the saved pipeline
loan_model_path = "model/loan_eligibility.joblib"
loan_pipeline = joblib.load(loan_model_path)


@router.post("/loan", response_model=LoanResponse, summary="Predict loan approval")
def predict_loan(payload: LoanApplication):
    """
    Predict loan approval based on applicant financial and demographic data.
    Uses a trained ML pipeline with preprocessing and classification steps.
    """

    #DataFrame from payload entries
    data = pd.DataFrame([{
        "Gender": payload.Gender,
        "Married": payload.Married,
        "Dependents": payload.Dependents,
        "Education": payload.Education,
        "Self_Employed": payload.Self_Employed,
        "ApplicantIncome": payload.ApplicantIncome,
        "CoapplicantIncome": payload.CoapplicantIncome,
        "LoanAmount": payload.LoanAmount,
        "Loan_Amount_Term": payload.Loan_Amount_Term,
        "Credit_History": payload.Credit_History,
        "Property_Area": payload.Property_Area,
    }])

    #prediction from the model(saved)
    prediction = loan_pipeline.predict(data)[0]

    #calculate the probability
    try:
        probability = loan_pipeline.predict_proba(data)[0][1]
    except AttributeError:
        probability = float(prediction)

    #converting number to status
    status = "Approved" if prediction == 1 else "Rejected"

    return {
        "approval_status": status,
        "probability": float(probability)
    }
