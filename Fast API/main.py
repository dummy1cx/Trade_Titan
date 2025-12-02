from fastapi import FastAPI
from app.api import loan_router, stock_router, insurance_router

## ---------------------------------------------------------
# Connection of end points with version control system
## All the sub routers are connected together with each other for LLM HTTP GET requests
## ---------------------------------------------------------
app = FastAPI(
    title="ML FastAPI — Multi-Model Prediction System",
    description="""
    This API serves three predictive machine learning models:

    1.Loan Eligibility Predictor — Predicts loan approval based on applicant data.  
    2.Stock Price Predictor (LSTM)— Predicts next-day close price using 5 days of OHLCV data.  
    3.Insurance Premium Predictor— Estimates premium cost based on demographic and lifestyle features.
    """,
    version="1.0.0",
    contact={
        "name": "Abhishek Das",
        "email": "dummy1cx@gmail.com"
    }
)

## ---------------------------------------------------------
## Connecting all three routers at main end point
## ---------------------------------------------------------
app.include_router(loan_router.router)
app.include_router(stock_router.router)
app.include_router(insurance_router.router)

## ---------------------------------------------------------
## Route for API Health Check 
## ---------------------------------------------------------
@app.get("/", tags=["Health Check"])
def root():
    return {
        "message": "ML FastAPI is running",
        "endpoints": {
            "loan_predictor": "/predict/loan",
            "stock_predictor": "/predict/stock",
            "insurance_predictor": "/predict/insurance"
        }
    }
