# Tool_stock performs API call from Alphavantage to retrive last 5 days stock price for model inferencing
# For this integration I have taken help from ChatGPT and Gemini

from __future__ import annotations
import os, time
from typing import List, Dict, Any
import requests

# API integration for tool calling
try:
    from app import settings
    ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", settings.ALPHAVANTAGE_API_KEY)
    PREDICT_BASE_URL = os.getenv("PREDICT_BASE_URL") or getattr(settings, "PREDICT_BASE_URL", "http://98.84.110.6:8000")
except Exception:
    ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY", "")
    PREDICT_BASE_URL = os.getenv("PREDICT_BASE_URL", "http://98.84.110.6:8000")

ALPHAVANTAGE_URL = "https://www.alphavantage.co/query"  ## Stock information
TIMEOUT = 15

def _av_call(params: Dict[str, Any]) -> Dict[str, Any]:
    delay = 1.0
    for attempt in range(4):
        r = requests.get(ALPHAVANTAGE_URL, params=params, timeout=TIMEOUT)
        if r.status_code == 200:
            return r.json()
        if r.status_code in (429, 500, 502, 503, 504) and attempt < 3:
            time.sleep(delay); delay = min(delay * 2, 6.0); continue
        r.raise_for_status()
    raise RuntimeError("Alpha Vantage request failed after retries")

def _fetch_daily_series(symbol: str) -> Dict[str, Dict[str, str]]:
    
    if not ALPHAVANTAGE_API_KEY:
        raise RuntimeError("Missing ALPHAVANTAGE_API_KEY.")
    # Daily data for stocks
    daily = _av_call({
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": ALPHAVANTAGE_API_KEY,
        "outputsize": "compact",
    })
    for k in daily.keys():
        if "Time Series (Daily)" in k:
            return daily[k]

    # Exception Check
    adjusted = _av_call({
        "function": "TIME_SERIES_DAILY_ADJUSTED",
        "symbol": symbol,
        "apikey": ALPHAVANTAGE_API_KEY,
        "outputsize": "compact",
    })
    for k in adjusted.keys():
        if "Time Series (Daily)" in k:
            return adjusted[k]

    # Displaying reason if results not found
    msg = daily.get("Note") or daily.get("Information") or daily.get("Error Message") \
          or adjusted.get("Note") or adjusted.get("Information") or adjusted.get("Error Message") \
          or "No time series in response"
    raise ValueError(f"Alpha Vantage did not return a daily series. Detail: {msg}")

def _extract_last_n(series: Dict[str, Dict[str, str]], n: int = 5) -> List[Dict[str, float]]:
    # dates in reverse order for model feeding
    dates = sorted(series.keys(), reverse=True)[:n]
    dates.reverse()
    out: List[Dict[str, float]] = []
    for d in dates:
        row = series[d]
        # daily 1 high 2 low 3 close 4 volume 5
        open_v   = float(row.get("1. open") or row.get("1. Open"))
        high_v   = float(row.get("2. high") or row.get("2. High"))
        low_v    = float(row.get("3. low")  or row.get("3. Low"))
        close_v  = float(row.get("4. close") or row.get("4. Close"))
        volume_v = int(float(row.get("5. volume") or row.get("6. volume") or 0))
        out.append({"open": open_v, "high": high_v, "low": low_v, "close": close_v, "volume": volume_v})
    if len(out) < n:
        raise ValueError(f"Only {len(out)} trading days available; need {n}")
    return out

def _predict_with_service(ticker: str, window: List[Dict[str, float]]) -> Dict[str, Any]:
    url = f"{PREDICT_BASE_URL}/predict/stock"
    payload = {"ticker": ticker.upper(), "window_size": len(window), "data": window}
    r = requests.post(url, json=payload, timeout=TIMEOUT)
    if r.status_code >= 400:
        try: detail = r.json()
        except Exception: detail = r.text
        raise RuntimeError(f"Stock predictor HTTP {r.status_code}: {detail}")
    return r.json()

def forecast_next_close(ticker: str, days: int = 5) -> Dict[str, Any]:
    series = _fetch_daily_series(ticker)
    window = _extract_last_n(series, n=days)
    pred = _predict_with_service(ticker, window)
    return {
        "type": "stock_forecast",
        "ticker": pred.get("ticker", ticker.upper()),
        "predicted_close": float(pred.get("predicted_close")),
        "window_used": len(window),
        "data_points": len(window),
        "source": "alphavantage+daily+lstm",
        "service_url": f"{PREDICT_BASE_URL}/predict/stock",
    }

# test_2
if __name__ == "__main__":
    import argparse, json
    p = argparse.ArgumentParser()
    p.add_argument("--ticker", required=True)
    p.add_argument("--days", type=int, default=5)
    args = p.parse_args()
    print(json.dumps(forecast_next_close(args.ticker, days=args.days), indent=2))