from fastapi import APIRouter
from app.schemas.read_schemas import StockInput, StockResponse
import torch
import torch.nn as nn
import numpy as np
import joblib

router = APIRouter(prefix="/predict", tags=["Stock Predictor"])
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# -----------------------------
# LSTM Model Definition
# -----------------------------
class LSTMModel(nn.Module):
    def __init__(self, input_size=5, hidden_size=64, num_layers=3, dropout=0.2):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout
        )
        self.fc = nn.Linear(hidden_size, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = out[:, -1, :]
        return self.fc(out)

# -----------------------------
# Load model + scalers
# -----------------------------
scalers = joblib.load("model/stock_pred_scalers.joblib")
X_scaler = scalers["X_scaler"]
y_scaler = scalers["y_scaler"]

model = LSTMModel(input_size=5, hidden_size=64, num_layers=3, dropout=0.2)
model.load_state_dict(torch.load("model/stock_prediction.pth", map_location=device))
model.to(device)
model.eval()

# -----------------------------
# Endpoint
# -----------------------------
@router.post("/stock", response_model=StockResponse, summary="Predict next-day stock close price")
def predict_stock(payload: StockInput):
    data = np.array([[d.open, d.high, d.low, d.close, d.volume] for d in payload.data])
    scaled_input = X_scaler.transform(data)
    x_tensor = torch.tensor(scaled_input, dtype=torch.float32).unsqueeze(0).to(device)

    with torch.no_grad():
        pred_scaled = model(x_tensor).cpu().numpy().reshape(-1, 1)
    pred_price = y_scaler.inverse_transform(pred_scaled).ravel()[0]

    return {"ticker": payload.ticker, "predicted_close": float(pred_price)}
