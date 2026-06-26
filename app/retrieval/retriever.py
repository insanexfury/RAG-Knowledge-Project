from app.retrieval.vector_store import VectorStore
from app.embeddings.embedder import Embedder
from app.core.config import settings
from app.retrieval.reranker import Reranker
class Retriever:
    def __init__(self, vector_store: VectorStore, embedder: Embedder, reranker:Reranker):
        """"""
        self.embedder = embedder
        self.vector_store=vector_store
        self.reranker=reranker
        
    def retrieve(self, query: str, top_k: int =None) -> list[dict]: 
        """"""
        query_vector = self.embedder.embed_query(query)
        query_vector = query_vector.reshape(1, -1)
        if top_k is None:
            top_k = settings.top_k
        top_k_initial = top_k *4 
        distances,indices = self.vector_store.index.search(query_vector ,top_k_initial)
        retrieved_data=[]
        for distance,index in zip(distances[0] , indices[0]):
            if distance < 0.3:
                continue
            chunk = self.vector_store.metadata[index]
            retrieved_data.append({
                                "text":chunk["text"],
                                "metadata":chunk["metadata"],
                                "score":float(distance)})
        retrieved_data = self.reranker.rerank(query,retrieved_data,top_k)
        return retrieved_data