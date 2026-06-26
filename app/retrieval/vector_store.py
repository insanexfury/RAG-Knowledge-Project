from pathlib import Path
import faiss
import numpy as np
import json

class VectorStore:
    """A simple in-memory vector store for storing document embeddings and metadata."""
    def __init__(self):
        self.vectors = None
        self.index=None
        self.metadata = []
    
    def add_chunks(self, embedded_chunks: list[dict]) -> None:
        """Add chunks to existing index without overwriting."""
        vectors = np.array([chunk["embedding"] for chunk in embedded_chunks]).astype(np.float32)
        dim = vectors.shape[1]
        if self.index is None:
            self.index = faiss.IndexFlatIP(dim)
        self.index.add(vectors)
        self.metadata.extend([
            {k: v for k, v in chunk.items() if k != "embedding"}
            for chunk in embedded_chunks
        ])
    def save(self, index_path: Path ,metadata_path: Path) ->  None:
        """Saves the Faiss index file and Metadata list"""
        faiss.write_index(self.index,str(index_path))
        with open(metadata_path, "w") as f:
            json.dump(self.metadata, f)
        
    def load(self, index_path: Path, metadata_path: Path ) -> None:
        """Load the FAISS index and metadata from disk."""
        self.index = faiss.read_index(str(index_path)) 
        with open(metadata_path,"r") as f:
            self.metadata =  json.load(f)
        
        
        