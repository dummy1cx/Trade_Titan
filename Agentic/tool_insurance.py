from __future__ import annotations
import os, requests

# API call from oublic IP
try:
    from app import settings
    PREDICT_BASE_URL = os.getenv("PREDICT_BASE_URL") or getattr(settings, "PREDICT_BASE_URL", "http://98.84.110.6:8000")
except Exception:
    PREDICT_BASE_URL = os.getenv("PREDICT_BASE_URL", "http://98.84.110.6:8000")

TIMEOUT = 15

def quote_premium(*, age: int, sex: str, bmi: float, children: int, smoker: str, region: str):
    
    url = f"{PREDICT_BASE_URL}/predict/insurance"
    payload = {
        "age": age,
        "sex": sex,
        "bmi": bmi,
        "children": children,
        "smoker": smoker,
        "region": region,
    }
    r = requests.post(url, json=payload, timeout=TIMEOUT)
    if r.status_code >= 400:
        try: detail = r.json()
        except Exception: detail = r.text
        raise RuntimeError(f"Insurance predictor HTTP {r.status_code}: {detail}")
    data = r.json()
    return {
        "type": "insurance_quote",
        "predicted_premium": float(data.get("predicted_premium")),
        "model_version": data.get("model_version", "unknown"),
        "service_url": url,
    }

if __name__ == "__main__":
    import argparse, json
    p = argparse.ArgumentParser()
    p.add_argument("--age", type=int, required=True)
    p.add_argument("--sex", required=True, choices=["male","female"])
    p.add_argument("--bmi", type=float, required=True)
    p.add_argument("--children", type=int, required=True)
    p.add_argument("--smoker", required=True, choices=["yes","no"])
    p.add_argument("--region", required=True, choices=["southeast","southwest","northeast","northwest"])
    args = p.parse_args()
    out = quote_premium(age=args.age, sex=args.sex, bmi=args.bmi, children=args.children, smoker=args.smoker, region=args.region)
    print(json.dumps(out, indent=2))