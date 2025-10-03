from fastapi import FastAPI
from app.api import predict

app = FastAPI(
    title="Loan Approval Prediction API",
    version="1.0.0",
    description="A FastAPI app that predicts loan approval using a trained Random Forest model",
)

@app.get("/", tags=["Root"])
def read_root():
    return {
        "message": "Welcome to the Loan Approval Prediction API",
        "try": "POST /api/predict",
        "docs": "/docs"
    }

app.include_router(predict.router, prefix="/api")
