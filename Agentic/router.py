## most of the code from router.py is directly taken from ChatGPT as I could not fix the bugs in the code
from __future__ import annotations


import re
from typing import Dict, Any, List, Optional

STOCK_INTENT    = "stock_forecast"     #### The router will decide 
INS_INTENT      = "insurance_quote"    #### From the intent
LOAN_INTENT     = "loan_approval"      ### Whether it is loan insurance stock or talk
RAG_INTENT      = "rag_answer"
SMALLTALK_INTENT = "smalltalk"  

INS_REQUIRED = ["age", "sex", "bmi", "children", "smoker", "region"]
LOAN_REQUIRED = [
    "Gender", "Married", "Dependents", "Education", "Self_Employed",
    "ApplicantIncome", "CoapplicantIncome", "LoanAmount",
    "Loan_Amount_Term", "Credit_History", "Property_Area",
]

COMMON_UPPER = {"USD","CEO","CFO","IPO","EPS","GAAP","IFRS","ROI","VAT","APAC","EMEA","USA","UK","EU"}

def has_any(text: str, kws: List[str]) -> bool:
    t = text.lower()
    return any(k in t for k in kws)

def is_smalltalk(text: str) -> bool:
    t = (text or "").strip().lower()
    if not t:
        return False
    if len(t) <= 8:  
        return True
    greetings = (
        "hi", "hello", "hey", "yo",  ### For small talk with the model
        "thanks", "thank you",
        "good morning", "good evening", "good night",
        "who are you", "help", "what can you do"
    )
    return any(t == g or t.startswith(g) for g in greetings)

def extract_keyvals_freeform(text: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for m in re.finditer(r'(\b[\w\.]+)\s*[:=]\s*([-\w\.]+)', text):
        k, v = m.group(1), m.group(2)
        out[k] = v
    return out

def maybe_int(v: Any) -> Optional[int]:
    try: return int(v)
    except Exception: return None

def maybe_float(v: Any) -> Optional[float]:
    try: return float(v)
    except Exception: return None

def extract_ticker(text: str) -> Optional[str]:
    m = re.search(r'(?:ticker|symbol)\s*[:=]\s*([A-Za-z\.\-]{1,6})', text, flags=re.I)
    if m: return m.group(1).upper()
    m = re.search(r'\$([A-Za-z]{1,5})\b', text)
    if m: return m.group(1).upper()
    candidates = re.findall(r'\b[A-Z]{1,5}\b', text)
    for c in candidates:
        if c not in COMMON_UPPER and not c.isdigit():
            return c
    return None

def extract_insurance_slots(text: str, params: Dict[str, Any]) -> Dict[str, Any]:
    kv = extract_keyvals_freeform(text)
    out = dict(params) if params else {}
    if "age" in kv and "age" not in out: out["age"] = _maybe_int(kv["age"])
    if "bmi" in kv and "bmi" not in out: out["bmi"] = _maybe_float(kv["bmi"])
    if "children" in kv and "children" not in out: out["children"] = _maybe_int(kv["children"])
    for k in ("sex","smoker","region"):
        if k in kv and k not in out: out[k] = kv[k].lower()
    m = re.search(r'\bage\s+(\d{1,3})\b', text, flags=re.I)
    if "age" not in out and m: out["age"] = int(m.group(1))
    m = re.search(r'\bbmi\s+(\d+(\.\d+)?)\b', text, flags=re.I)
    if "bmi" not in out and m: out["bmi"] = float(m.group(1))
    m = re.search(r'\bchildren\s+(\d{1,2})\b', text, flags=re.I)
    if "children" not in out and m: out["children"] = int(m.group(1))
    if "smoker" not in out and _has_any(text, ["smoker yes","smokes","smoker:yes","smoker=yes"]): out["smoker"] = "yes"
    if "smoker" not in out and _has_any(text, ["smoker no","non-smoker","smoker:no","smoker=no"]): out["smoker"] = "no"
    return out

def extract_loan_slots(text: str, params: Dict[str, Any]) -> Dict[str, Any]:
    kv = extract_keyvals_freeform(text)
    out = dict(params) if params else {}
    for k in LOAN_REQUIRED:
        if k in kv and k not in out:
            out[k] = kv[k]
    for k in ("ApplicantIncome","CoapplicantIncome","LoanAmount","Loan_Amount_Term","Credit_History","Dependents"):
        if k in out: continue
        if k in kv:
            out[k] = maybe_float(kv[k]) if k != "Dependents" else maybe_int(kv[k])
    return out

def route(message: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    msg = (message or "").strip()
    base_params = dict(params) if params else {}

    #small talk like hi hello response 
    if is_smalltalk(msg):
        return {"intent": SMALLTALK_INTENT, "missing": [], "params": {}}

    # intent from th eprompt
    is_stock = has_any(msg, ["predict","forecast","price","close","tomorrow","next day","next close","stock"])
    is_ins   = has_any(msg, ["insurance","premium","quote"])
    is_loan  = has_any(msg, ["loan","approve","approval","eligibility","emi"])

    if is_ins and not (is_stock or is_loan):
        intent = INS_INTENT
    elif is_loan and not is_stock:
        intent = LOAN_INTENT
    elif is_stock:
        intent = STOCK_INTENT
    else:
        intent = RAG_INTENT

    out_params: Dict[str, Any] = dict(base_params)

    if intent == STOCK_INTENT:
        if not out_params.get("ticker"):
            tk = extract_ticker(msg)
            if tk: out_params["ticker"] = tk
        missing = [] if out_params.get("ticker") else ["ticker"]
        return {"intent": intent, "missing": missing, "params": out_params}

    if intent == INS_INTENT:
        out_params = extract_insurance_slots(msg, out_params)
        missing = [k for k in INS_REQUIRED if out_params.get(k) in (None, "", [])]
        return {"intent": intent, "missing": missing, "params": out_params}

    if intent == LOAN_INTENT:
        out_params = extract_loan_slots(msg, out_params)
        missing = [k for k in LOAN_REQUIRED if out_params.get(k) in (None, "", [])]
        return {"intent": intent, "missing": missing, "params": out_params}

    # RAG fallback from the model
    return {"intent": RAG_INTENT, "missing": [], "params": out_params}

if __name__ == "__main__":
    import argparse, json
    p = argparse.ArgumentParser()
    p.add_argument("--q", required=True, help="user message")
    p.add_argument("--param", action="append", default=[], help="key=value (repeatable)")
    args = p.parse_args()
    pref: Dict[str, Any] = {}
    for kv in args.param:
        if "=" in kv:
            k, v = kv.split("=", 1)
            pref[k] = v
    print(json.dumps(route(args.q, params=pref), indent=2))