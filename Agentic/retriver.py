## -------------------------------------------------------
## This is code is used from OpenAI ChatGPT
## There was problem with my FAISS index with embedding
## WHich I could not fix
## Hence took help from Chatgpt
## ========================================================
from __future__ import annotations
import os
from typing import List, Dict, Optional
import json

import numpy as np
import pandas as pd
import faiss

from app.settings import OPENAI_API_KEY, KB_INDEX_PATH, KB_PARQUET_PATH

EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")
TOP_K = int(os.getenv("RETRIEVAL_K", "30"))

_openai_client = None
def _get_openai():
    global _openai_client
    if _openai_client is None:
        from openai import OpenAI
        _openai_client = OpenAI(api_key=OPENAI_API_KEY)
    return _openai_client

_df: Optional[pd.DataFrame] = None
_index: Optional[faiss.Index] = None

def _coerce_emb(v):
    
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return None
    if isinstance(v, list):
        return v
    if isinstance(v, np.ndarray):
        return v.astype(np.float32).tolist()
    if isinstance(v, (bytes, bytearray)):
        try:
            return json.loads(v.decode("utf-8"))
        except Exception:
            return None
    if isinstance(v, str):
        s = v.strip()
        if s.startswith("[") and s.endswith("]"):
            try:
                return json.loads(s)
            except Exception:
                return None
    return None

def _load():
    global _df, _index
    if _df is None:
        df = pd.read_parquet(KB_PARQUET_PATH)

        
        if "id" in df.columns:
            df = df.set_index("id", drop=False)

        
        if "embedding" not in df.columns:
            raise RuntimeError("Parquet missing 'embedding' column")
        df["embedding"] = df["embedding"].apply(_coerce_emb)

        
        mask = df["embedding"].apply(lambda v: isinstance(v, list) and len(v) > 0)
        df = df[mask].copy()

        
        for col, default in [("doc_title",""), ("filename",""), ("section",""),
                             ("page_start",None), ("text",None), ("text_clean",None)]:
            if col not in df.columns:
                df[col] = default

        _df = df

    if _index is None:
        _index = faiss.read_index(KB_INDEX_PATH)
        if _index.ntotal <= 0:
            raise RuntimeError("FAISS index has no vectors. Rebuild your index.")

    return _df, _index

def _l2_normalize(x: np.ndarray) -> np.ndarray:
    n = np.linalg.norm(x)
    return x if n == 0.0 else x / n

def embed_query(text: str) -> np.ndarray:
    client = _get_openai()
    v = client.embeddings.create(model=EMBED_MODEL, input=[text]).data[0].embedding
    v = np.asarray(v, dtype=np.float32)
    v = _l2_normalize(v)
    return v.reshape(1, -1)

def _citation(row: pd.Series) -> str:
    title = (str(row.get("doc_title")) or str(row.get("filename")) or "").strip()
    section = (str(row.get("section")) or "").strip()
    page = row.get("page_start", "")
    if page is None: page = ""
    if title and section and page != "":  return f"[{title} · {section} · p.{page}]"
    if title and page != "":              return f"[{title} · p.{page}]"
    return f"[{title}]" if title else "[Citation]"

def _snippet(text: str, limit: int = 600) -> str:
    t = (text or "").strip().replace("\n", " ")
    return t if len(t) <= limit else t[:limit] + "…"

def _rows_by_ids(df: pd.DataFrame, ids: np.ndarray) -> List[pd.Series]:
    out = []
    for _id in ids:
        if _id == -1:
            continue
        if _id in df.index:
            out.append(df.loc[_id])
        else:
            
            try:
                out.append(df.iloc[int(_id)])
            except Exception:
                continue
    return out

def retrieve(query: str, k: int = TOP_K) -> Dict[str, List[Dict]]:
    df, index = _load()

    q = embed_query(query)
    
    if q.shape[1] != index.d:
        raise RuntimeError(f"Embed dim {q.shape[1]} != index dim {index.d}. "
                           "Ensure EMBED_MODEL matches the model used to build the index.")

    sims, ids = index.search(q, k)
    sims, ids = sims[0], ids[0]

    rows = _rows_by_ids(df, ids)
    results = []
    for row, sim in zip(rows, sims[:len(rows)]):
        text = row.get("text") or row.get("text_clean") or ""
        results.append({
            "id": int(row.name),
            "score": float(sim),
            "doc_title": row.get("doc_title", row.get("filename","")),
            "section": row.get("section",""),
            "page": int(row.get("page_start",-1)) if pd.notna(row.get("page_start",None)) else None,
            "snippet": _snippet(str(text)),
            "citation": _citation(row),
        })

    results.sort(key=lambda r: r["score"], reverse=True)
    return {"snippets": results}

def retrieve_one(query: str, k: int = TOP_K) -> Dict[str, any]:
    out = retrieve(query, k=k)
    snips = out["snippets"]
    if not snips:
        return {"id": None, "score": 0.0, "snippet": "", "citation": ""}
    best = snips[0]
    return {
        "id": best["id"],
        "score": best["score"],
        "snippet": best["snippet"],
        "citation": best["citation"],
    }

if __name__ == "__main__":
    import argparse, json
    p = argparse.ArgumentParser()
    p.add_argument("--q", required=True)
    p.add_argument("--k", type=int, default=TOP_K)
    p.add_argument("--one", action="store_true")
    args = p.parse_args()

    print(json.dumps(
        retrieve_one(args.q, k=args.k) if args.one else retrieve(args.q, k=args.k),
        ensure_ascii=False, indent=2
    ))