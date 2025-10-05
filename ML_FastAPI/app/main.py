from fastapi import FastAPI
from app.api import loan_router, stock_router, insurance_router

# ---------------------------------------------------------
# Initialize the FastAPI app
# ---------------------------------------------------------
app = FastAPI(
    title="ML FastAPI — Multi-Model Prediction System",
    description="""
    This API serves three predictive machine learning models:

    • **Loan Eligibility Predictor** — Predicts loan approval based on applicant data.  
    • **Stock Price Predictor (LSTM)** — Predicts next-day close price using 5 days of OHLCV data.  
    • **Insurance Premium Predictor** — Estimates premium cost based on demographic and lifestyle features.
    """,
    version="1.0.0",
    contact={
        "name": "Abhishek Das",
        "email": "dummy1cx@gmail.com"
    }
)

# ---------------------------------------------------------
# Register Routers
# ---------------------------------------------------------
app.include_router(loan_router.router)
app.include_router(stock_router.router)
app.include_router(insurance_router.router)

# ---------------------------------------------------------
# Health Check Route
# ---------------------------------------------------------
@app.get("/", tags=["Health Check"])
def root():
    return {
        "message": "ML FastAPI is running 🚀",
        "endpoints": {
            "loan_predictor": "/predict/loan",
            "stock_predictor": "/predict/stock",
            "insurance_predictor": "/predict/insurance"
        }
    }
