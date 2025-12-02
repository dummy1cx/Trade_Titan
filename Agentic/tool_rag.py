# Orchestraing tool RAG with knowldge base

from __future__ import annotations
from typing import Dict, Any, List

from app.retriever import retrieve_one, retrieve
from app.finalizer import finalize_answer


def preview(query: str, k: int = 30) -> Dict[str, Any]:
   
    r = retrieve_one(query=query, k=k)
    return {
        "type": "rag_preview",
        "query": query,
        "score": float(r.get("score", 0.0)),
        "low_confidence": bool(r.get("low_confidence", False)),
        "snippet": (r.get("snippet") or "").strip(),
        "citation": (r.get("citation") or "").strip(),
        "diagnostics": r.get("diagnostics", {}),
    }


def answer(query: str, k: int = 30) -> Dict[str, Any]:
    
    # pulls a few citations 
    r_all = retrieve(query=query, k=k)
    citations: List[str] = r_all.get("citations", [])[:3]

    text = finalize_answer(query=query, k=k)

    return {
        "type": "rag_answer",
        "query": query,
        "text": text,
        "citations": citations,
        "diagnostics": r_all.get("diagnostics", {}),
    }


# Conducting a smoke test
if __name__ == "__main__":
    import argparse, json
    p = argparse.ArgumentParser()
    p.add_argument("--q", required=True, help="question")
    p.add_argument("--k", type=int, default=30)
    p.add_argument("--mode", choices=["preview", "answer"], default="answer")
    args = p.parse_args()

    if args.mode == "preview":
        out = preview(args.q, k=args.k)
    else:
        out = answer(args.q, k=args.k)

    print(json.dumps(out, ensure_ascii=False, indent=2))