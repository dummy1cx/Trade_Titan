from pydantic import BaseModel
from typing import List, Optional

# ------------------------------------------
# Pudantic Input Schemas for Data Validation
# ------------------------------------------

class LoanApplication(BaseModel):
    """Input schema for predicting loan approval based on applicant details."""
    Gender: str
    Married: str
    Dependents: int                 ## The API expects data in this format
    Education: str
    Self_Employed: str
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: float
    Property_Area: str


class LoanResponse(BaseModel):
    """Output schema for loan approval prediction."""
    approval_status: str                 
    probability: float                   
    model_version: Optional[str] = "LoanModel_v1"


# --------------------------
# Stock Price Predictor (LSTM)
# ------------------------------

class StockDay(BaseModel):
    """Represents one day's OHLCV data."""
    open: float
    high: float
    low: float
    close: float
    volume: float


class StockInput(BaseModel):
    """Input data for predicting next-day close price using last 5 days of OHLCV data."""
    ticker: Optional[str] = "SP500"  
    window_size: int = 5 ## The model waas trained with 5 days window
    data: List[StockDay]                 


class StockResponse(BaseModel):
    """Output formatfor stock price prediction."""
    ticker: str
    predicted_close: float
    model_version: Optional[str] = "LSTM_3Layer_v1"


# ------------------------------------
# Insurance Premium Predictor (XGBoost)
# ----------------------------------------

class InsuranceInput(BaseModel):
    """Input schema for predicting insurance premium based on customer demographics."""
    age: int
    sex: str
    bmi: float
    children: int
    smoker: str
    region: str


class InsuranceResponse(BaseModel):
    """Output schema for insurance premium prediction."""
    predicted_premium: float
    model_version: Optional[str] = "XGB_Insurance_v1"
