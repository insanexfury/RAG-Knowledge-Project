from pathlib import Path
from app.embeddings.embedder import Embedder
from app.retrieval.vector_store import VectorStore
from app.retrieval.retriever import Retriever
from app.llm.generator import Generator
from app.retrieval.reranker import Reranker
from app.ingestion.pdf_extracter import load_pdf
from app.ingestion.preprocess import preprocess_pages
from app.ingestion.chunking import chunk_pages
from app.core.config import settings
import json

class RagPipeline:
    def __init__(self):
        """_summary_
        """
        self.embedder = Embedder()
        self.vector_store = VectorStore()
        self.reranker = Reranker()
        self.retriever = Retriever(self.vector_store, self.embedder,self.reranker)
        self.generator = Generator()
        self.document_registry ={}
        settings.index_dir.mkdir(parents=True, exist_ok=True)
        index_path = settings.index_dir / "index.faiss"
        metadata_path = settings.index_dir / "metadata.json"
        if index_path.exists() and metadata_path.exists():
            self.vector_store.load(index_path, metadata_path)
        registry_path = settings.index_dir / "registry.json"
        if registry_path.exists():
            with open(registry_path, "r") as f:
                self.document_registry = json.load(f)
        
    def ingest(self, file_path: Path) -> int:
        if file_path.name in self.document_registry:
            raise ValueError(f"{file_path.name} is already in registry")
        pages = load_pdf(file_path)
        cleaned_pages = preprocess_pages(pages)
        chunked_pages = chunk_pages(cleaned_pages)
        embedding = self.embedder.embed_chunks(chunked_pages)
        self.vector_store.add_chunks(embedding)
        self.vector_store.save(
            settings.index_dir / "index.faiss",
            settings.index_dir / "metadata.json"
        )
        self.document_registry[file_path.name] = len(embedding)
        with open(settings.index_dir / "registry.json", "w") as f:
            json.dump(self.document_registry, f)
        return len(embedding)
    
    def query(self, question:str) ->dict:
        retrieved = self.retriever.retrieve(question)
        answer = self.generator.generate(question,retrieved)
        return {"answer":answer , "retrieved_chunks":retrieved}
        