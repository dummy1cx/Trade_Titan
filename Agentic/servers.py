## FOR API servers i took help from code assitance from ChatGPT

from __future__ import annotations

import json
from typing import Any, Dict, Optional, Generator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# non streaming response
from app.agent_graph import run_chat

# validate the router with intent in the query
from app.router import (
    route as rule_route,
    STOCK_INTENT, INS_INTENT, LOAN_INTENT, RAG_INTENT, SMALLTALK_INTENT,
)

# tools integration total 4 tools
from app.tool_stock import forecast_next_close
from app.tool_insurance import quote_premium
from app.tool_loan import evaluate_loan
from app.tool_rag import preview as rag_preview, answer as rag_answer

# NLG streaming / freeform
from app.nlg import (
    stream_from_tool,
    speak_freeform,
    stream_from_evidence,  
)

app = FastAPI(title="Finance Agent API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    params: Optional[Dict[str, Any]] = None

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/chat")
def chat(req: ChatRequest):
    """Non-streaming chat: runs your LangGraph and returns a structured answer."""
    return run_chat(req.message, params=req.params or {})

@app.post("/chat/stream")
def chat_stream(req: ChatRequest):
    """
    Streaming (SSE). Tools run synchronously; then we stream only the final surface form.
    Client must consume Server-Sent Events.
    """
    decision = rule_route(req.message, params=req.params or {})
    intent = decision["intent"]
    missing = decision["missing"]
    params  = decision["params"]

    def sse() -> Generator[str, None, None]:
       
        yield f"event: meta\ndata: {json.dumps({'intent': intent, 'missing': missing})}\n\n"

        
        if missing:
            msg = f"I can do that. I just need: {', '.join(missing)}."
            yield f"data: {msg}\n\n"
            yield "event: done\ndata: {}\n\n"
            return

        try:
            if intent == SMALLTALK_INTENT:
                
                text = speak_freeform(req.message)
                yield f"data: {text}\n\n"

            elif intent == STOCK_INTENT:
                payload = forecast_next_close(params["ticker"])
                for tok in stream_from_tool(req.message, intent, payload):
                    yield f"data: {tok}\n\n"

            elif intent == INS_INTENT:
                payload = quote_premium(
                    age=int(params["age"]),
                    sex=str(params["sex"]),
                    bmi=float(params["bmi"]),
                    children=int(params["children"]),
                    smoker=str(params["smoker"]),
                    region=str(params["region"]),
                )
                for tok in stream_from_tool(req.message, intent, payload):
                    yield f"data: {tok}\n\n"

            elif intent == LOAN_INTENT:
                payload = evaluate_loan(
                    Gender=params["Gender"],
                    Married=params["Married"],
                    Dependents=int(params["Dependents"]),
                    Education=params["Education"],
                    Self_Employed=params["Self_Employed"],
                    ApplicantIncome=float(params["ApplicantIncome"]),
                    CoapplicantIncome=float(params["CoapplicantIncome"]),
                    LoanAmount=float(params["LoanAmount"]),
                    Loan_Amount_Term=float(params["Loan_Amount_Term"]),
                    Credit_History=float(params["Credit_History"]),
                    Property_Area=params["Property_Area"],
                )
                for tok in stream_from_tool(req.message, intent, payload):
                    yield f"data: {tok}\n\n"

            else:  # RAG
                rag = rag_answer(req.message, k=30)
                text = (rag.get("text") or "").strip()
                cits = rag.get("citations", [])[:3]
                if cits and all(c not in text for c in cits):
                    text = f"{text}\n\n" + " ".join(cits)

                if not text:
                    yield "data: I couldn’t find evidence in the knowledge base for this question.\n\n"
                else:
                    
                    for chunk in _chunk_text(text, size=180):
                        yield f"data: {chunk}\n\n"

        except Exception as e:
            yield f"data: Something went wrong: {str(e)}\n\n"

       
        yield "event: done\ndata: {}\n\n"

 
    return StreamingResponse(
        sse(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
            "Access-Control-Allow-Origin": "*",  # handy for local dev
        },
    )

def _chunk_text(text: str, size: int = 180):
    """Yield text in ~size-char chunks on word boundaries."""
    s = text.strip()
    while len(s) > size:
        cut = s.rfind(" ", 0, size)
        if cut <= 0:
            cut = size
        yield s[:cut]
        s = s[cut:].lstrip()
    if s:
        yield s