import numpy as np
from sentence_transformers import SentenceTransformer
from app.core.config import settings

class Embedder:
    def __init__(self):
        # Initialize your embedding model here (e.g., load a pre-trained model)
        self.model = SentenceTransformer(settings.embeddings_model)
        
    def embed_chunks(self, chunks: list[dict]) -> list[dict]:
        chunk_texts = [chunk["text"] for chunk in chunks]
        chunk_embeddings = self.model.encode(chunk_texts, normalize_embeddings=True)
        return [{**chunk, "embedding": chunk_embeddings[i]} for i, chunk in enumerate(chunks)]
    
    def embed_query(self, query: str) -> np.ndarray:
        return self.model.encode([query],normalize_embeddings=True)[0]  # Example: returning the embedding vector of the query
    
_embedder = None
def get_embedder() -> Embedder:
    global _embedder
    if _embedder is None:
        _embedder = Embedder()
    return _embedder