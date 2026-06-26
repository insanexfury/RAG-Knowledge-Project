from sentence_transformers import CrossEncoder
from app.core.config import settings
class Reranker:
    
    def __init__(self):
        self.model = CrossEncoder(settings.cross_encoder_model)
        
    def rerank(self, query:str, chunks:list[dict], top_k=5) -> list[dict]:
        pairs =[[query,chunk["text"]] for chunk in chunks]
        scores = self.model.predict(pairs)
        reranked = [{**chunk, "rerank_score": float(score)} for chunk, score in zip(chunks, scores)]
        reranked.sort(key=lambda x: x["rerank_score"],reverse=True)
        return reranked[:top_k]