### This code was reference from CampusX online tutorial on Langgraph and ChatGPT

from __future__ import annotations
from typing import TypedDict, Dict, Any, Optional, List

from langgraph.graph import StateGraph, END

# Router + intents
from app.router import (
    route as rule_route,
    STOCK_INTENT,
    INS_INTENT,
    LOAN_INTENT,
    RAG_INTENT,
    SMALLTALK_INTENT,   
)


from app.tool_stock import forecast_next_close
from app.tool_insurance import quote_premium
from app.tool_loan import evaluate_loan
from app.tool_rag import answer as rag_answer

# NLG
from app.nlg import speak_from_tool, speak_freeform  


## SChema for Graph state
class GraphState(TypedDict, total=False):
    message: str
    params: Dict[str, Any]
    intent: str
    missing: List[str]

    tool_result: Dict[str, Any]
    rag_result: Dict[str, Any]
    citations: List[str]
    final_text: str

## Nodes for connecting the workflow
def route_node(state: GraphState) -> GraphState:
    decision = rule_route(state["message"], params=state.get("params") or {})
    state["intent"] = decision["intent"]
    state["missing"] = decision["missing"]
    state["params"] = decision["params"]
    return state

def stock_node(state: GraphState) -> GraphState:
    p = state.get("params", {})
    try:
        res = forecast_next_close(p["ticker"])
        state["tool_result"] = res
    except Exception as e:
        state["tool_result"] = {"type": "error", "reason": str(e)}
    return state

def insurance_node(state: GraphState) -> GraphState:
    p = state.get("params", {})
    try:
        res = quote_premium(
            age=int(p["age"]),
            sex=str(p["sex"]),
            bmi=float(p["bmi"]),
            children=int(p["children"]),
            smoker=str(p["smoker"]),
            region=str(p["region"]),
        )
        state["tool_result"] = res
    except Exception as e:
        state["tool_result"] = {"type": "error", "reason": str(e)}
    return state

def loan_node(state: GraphState) -> GraphState:
    p = state.get("params", {})
    try:
        res = evaluate_loan(
            Gender=p["Gender"],
            Married=p["Married"],
            Dependents=int(p["Dependents"]),
            Education=p["Education"],
            Self_Employed=p["Self_Employed"],
            ApplicantIncome=float(p["ApplicantIncome"]),
            CoapplicantIncome=float(p["CoapplicantIncome"]),
            LoanAmount=float(p["LoanAmount"]),
            Loan_Amount_Term=float(p["Loan_Amount_Term"]),
            Credit_History=float(p["Credit_History"]),
            Property_Area=p["Property_Area"],
        )
        state["tool_result"] = res
    except Exception as e:
        state["tool_result"] = {"type": "error", "reason": str(e)}
    return state

def rag_node(state: GraphState) -> GraphState:
    try:
        res = rag_answer(state["message"], k=30)   # already finalized answer text
        state["rag_result"] = res
        state["citations"] = res.get("citations", [])[:3]
    except Exception as e:
        state["rag_result"] = {"type": "error", "reason": str(e)}
        state["citations"] = []
    return state

def finalize_node(state: GraphState) -> GraphState:
    
    missing = state.get("missing") or []
    if missing:
        need = ", ".join(missing)
        state["final_text"] = f"I can do that. I just need: {need}."
        return state

    intent = state.get("intent")
    msg = state.get("message", "")

    
    if intent == SMALLTALK_INTENT:
        state["final_text"] = speak_freeform(msg)
        return state

    if intent == STOCK_INTENT:
        tr = state.get("tool_result", {})
        if tr.get("type") == "error":
            state["final_text"] = f"I couldn’t run the stock forecast: {tr.get('reason')}"
            return state
        state["final_text"] = speak_from_tool(msg, intent, tr)
        return state

    if intent == INS_INTENT:
        tr = state.get("tool_result", {})
        if tr.get("type") == "error":
            state["final_text"] = f"I hit a snag quoting the premium: {tr.get('reason')}"
            return state
        state["final_text"] = speak_from_tool(msg, intent, tr)
        return state

    if intent == LOAN_INTENT:
        tr = state.get("tool_result", {})
        if tr.get("type") == "error":
            state["final_text"] = f"I couldn’t score the loan right now: {tr.get('reason')}"
            return state
        state["final_text"] = speak_from_tool(msg, intent, tr)
        return state

    
    rr = state.get("rag_result", {})
    if rr.get("type") == "rag_answer":
        txt = (rr.get("text") or "").strip()
        cits = state.get("citations") or []
        if cits and all(c not in txt for c in cits):
            txt = f"{txt}\n\n" + " ".join(cits)
        state["final_text"] = txt or "No answer."
        return state

    # Error handling
    if rr.get("type") == "error":
        state["final_text"] = f"RAG error: {rr.get('reason')}"
        return state

    state["final_text"] = "I couldn’t produce an answer."
    return state

## Agentic Graph implementations
def build_graph():
    g = StateGraph(GraphState)

    g.add_node("route", route_node)
    g.add_node("stock", stock_node)
    g.add_node("insurance", insurance_node)
    g.add_node("loan", loan_node)
    g.add_node("rag", rag_node)
    g.add_node("finalize", finalize_node)

    g.set_entry_point("route")

    def _branch_missing(state: GraphState) -> str:
        if state.get("missing"):
            return "finalize"
        intent = state.get("intent")
        if intent == SMALLTALK_INTENT:
            return "finalize"
        if intent == STOCK_INTENT:
            return "stock"
        if intent == INS_INTENT:
            return "insurance"
        if intent == LOAN_INTENT:
            return "loan"
        return "rag"

    g.add_conditional_edges(
        "route",
        _branch_missing,
        {
            "finalize": "finalize",
            "stock": "stock",
            "insurance": "insurance",
            "loan": "loan",
            "rag": "rag",
        },
    )

    g.add_edge("stock", "finalize")
    g.add_edge("insurance", "finalize")
    g.add_edge("loan", "finalize")
    g.add_edge("rag", "finalize")
    g.add_edge("finalize", END)

    return g.compile()

## Chat for small and casual conversation
def run_chat(message: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    app = build_graph()
    start: GraphState = {"message": message, "params": params or {}}
    out: GraphState = app.invoke(start)

    return {
        "answer": out.get("final_text", ""),
        "intent": out.get("intent", ""),
        "missing": out.get("missing", []),
        "tool_used": (
            "stock" if out.get("intent") == STOCK_INTENT
            else "insurance" if out.get("intent") == INS_INTENT
            else "loan" if out.get("intent") == LOAN_INTENT
            else "rag" if out.get("intent") == RAG_INTENT
            else "smalltalk" if out.get("intent") == SMALLTALK_INTENT
            else None
        ),
        "citations": out.get("citations", []) if out.get("intent") == RAG_INTENT else [],
    }


# smoke test

if __name__ == "__main__":
    import argparse, json
    p = argparse.ArgumentParser()
    p.add_argument("--q", required=True)
    args = p.parse_args()
    print(json.dumps(run_chat(args.q), ensure_ascii=False, indent=2))