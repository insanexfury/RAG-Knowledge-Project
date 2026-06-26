def format_citations(retrieved_chunks: list[dict]) -> list[dict]:
    """"""
    seen = {}
    results = []
    for chunks in retrieved_chunks:
        key =  chunks["metadata"]["source"], chunks["metadata"]["page_number"]
        if key not in seen or chunks.get("rerank_score", chunks["score"]) > seen[key].get("rerank_score", seen[key]["score"]):
            seen[key] = chunks
            
    sorted_citation = sorted(seen.values(), key=lambda x: x["rerank_score"], reverse=True)
    for chunks in sorted_citation:
        text = chunks["text"]
        if len(text) > 150:
            text = text[:150].rsplit(" ", 1)[0] + "..."
        results.append({
        "source": chunks["metadata"]["source"],
        "page_number": chunks["metadata"]["page_number"],
        "score": round(chunks.get("rerank_score",chunks["score"]), 2),
        "excerpt": text})
    return results