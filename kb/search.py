# semantic search over JSON knowledge base

import json
import os
from typing import List, Dict
from sklearn.metrics.pairwise import cosine_similarity

# try transformer embedding, if unavailable go for TF-IDF
try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")
    use_transformer = True
except Exception:
    use_transformer = False
    from sklearn.feature_extraction.text import TfidfVectorizer

kb_path = os.path.join(os.path.dirname(__file__), "kb.json")

# load kb
with open(kb_path, "r", encoding="utf-8") as f:
    kb = json.load(f)

# build embeddings for KB 
texts = [f"{item['title']} {' '.join(item['symptoms'])}" for item in kb] #can add category too for better accuracy

if use_transformer:
    emb = model.encode(texts, convert_to_numpy=True)
else:
    tfidf = TfidfVectorizer()
    emb = tfidf.fit_transform(texts).toarray()

# search func
def search_kb(query: str, top_k: int = 5) -> List[Dict]:
    if not query.strip():
        return []

    # embed query
    if use_transformer:
        q = model.encode([query], convert_to_numpy=True)
    else:
        q = tfidf.transform([query]).toarray()

    # compute similarity
    sims = cosine_similarity(q, emb)[0]
    ranked = sorted(
        [
            {**item, "score": float(sims[i])}
            for i, item in enumerate(kb)
        ],
        key=lambda x: x["score"],
        reverse=True
    )

    return ranked[:top_k]

