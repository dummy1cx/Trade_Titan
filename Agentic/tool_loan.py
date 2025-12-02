from __future__ import annotations
import os, requests

# API call with public IP
try:
    from app import settings
    PREDICT_BASE_URL = os.getenv("PREDICT_BASE_URL") or getattr(settings, "PREDICT_BASE_URL", "http://98.84.110.6:8000")
except Exception:
    PREDICT_BASE_URL = os.getenv("PREDICT_BASE_URL", "http://98.84.110.6:8000")

TIMEOUT = 15 ## WAIT and TIMEOUT

def evaluate_loan(
    *,
    Gender: str,
    Married: str,
    Dependents: int,
    Education: str,
    Self_Employed: str,
    ApplicantIncome: float,
    CoapplicantIncome: float,
    LoanAmount: float,
    Loan_Amount_Term: float,
    Credit_History: float,
    Property_Area: str,
):
   
    url = f"{PREDICT_BASE_URL}/predict/loan"
    payload = {
        "Gender": Gender,
        "Married": Married,
        "Dependents": Dependents,
        "Education": Education,
        "Self_Employed": Self_Employed,
        "ApplicantIncome": ApplicantIncome,
        "CoapplicantIncome": CoapplicantIncome,
        "LoanAmount": LoanAmount,
        "Loan_Amount_Term": Loan_Amount_Term,
        "Credit_History": Credit_History,
        "Property_Area": Property_Area,
    }
    r = requests.post(url, json=payload, timeout=TIMEOUT)
    if r.status_code >= 400:
        try: detail = r.json()
        except Exception: detail = r.text
        raise RuntimeError(f"Loan predictor HTTP {r.status_code}: {detail}")
    data = r.json()
    return {
        "type": "loan_approval",
        "status": data.get("approval_status"),
        "probability": float(data.get("probability", 0.0)),
        "service_url": url,
    }

if __name__ == "__main__":
    import argparse, json
    p = argparse.ArgumentParser()
    p.add_argument("--Gender", required=True, choices=["Male","Female"])
    p.add_argument("--Married", required=True, choices=["Yes","No"])
    p.add_argument("--Dependents", type=int, required=True)
    p.add_argument("--Education", required=True, choices=["Graduate","Not Graduate"])
    p.add_argument("--Self_Employed", required=True, choices=["Yes","No"])
    p.add_argument("--ApplicantIncome", type=float, required=True)
    p.add_argument("--CoapplicantIncome", type=float, required=True)
    p.add_argument("--LoanAmount", type=float, required=True)
    p.add_argument("--Loan_Amount_Term", type=float, required=True)
    p.add_argument("--Credit_History", type=float, required=True)
    p.add_argument("--Property_Area", required=True, choices=["Urban","Semiurban","Rural"])
    args = p.parse_args()
    out = evaluate_loan(**vars(args))
    print(json.dumps(out, indent=2))