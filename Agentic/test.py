
from app.retriever import _load, embed_query
df, index = _load()
print("faiss ntotal:", index.ntotal, "| df rows:", len(df), "| index dim:", index.d)

qv = embed_query("alphabet international risks")
D, I = index.search(qv, 5)
ids = I[0].tolist()
print("top-5 ids:", ids)
print("resolvable:", [i in df.index for i in ids])

for i in ids:
    if i in df.index:
        row = df.loc[i]
        title = row.get("doc_title", row.get("filename"))
        txt = (row.get("text") or row.get("text_clean") or "")[:400].replace("\n"," ")
        print("title:", title)
        print("snippet sample:", txt)
        break
else:
    print("no ids resolved into df — index ids != dataframe index")