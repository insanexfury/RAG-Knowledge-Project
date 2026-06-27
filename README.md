# RAG Knowledge Assistant

A retrieval-augmented generation system for querying PDF documents, 
built from scratch — no LangChain — with FAISS retrieval, cross-encoder 
reranking, and measured evaluation.

## Results

| Metric    | Without reranking | With reranking |
|-----------|-------------------|-----------------|
| Hit Rate  | 80%                | 90%             |
| MRR       | 0.65               | 0.72            |

Evaluated on a 10-question ground truth set built from the source document.

## Architecture

## High-Level Architecture

```text
                        ┌──────────────────────────────┐
                        │      Streamlit Frontend      │
                        │------------------------------│
                        │ • PDF Upload                │
                        │ • Chat Interface            │
                        │ • Session Chat History      │
                        │ • Source Viewer             │
                        └──────────────┬──────────────┘
                                       │
                                 REST API
                                       │
                        ┌──────────────▼──────────────┐
                        │        FastAPI App          │
                        │-----------------------------│
                        │  POST /ingest              │
                        │  POST /query               │
                        └──────────────┬──────────────┘
                                       │
                                       ▼
                        ┌─────────────────────────────┐
                        │        RagPipeline          │
                        └──────────────┬──────────────┘
                                       │
          ┌────────────────────────────┼────────────────────────────┐
          │                            │                            │
          ▼                            ▼                            ▼
 ┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
 │ Document Parser │         │ Retrieval Flow  │         │ Metadata Store  │
 ├─────────────────┤         ├─────────────────┤         ├─────────────────┤
 │ PDF Extraction  │         │ Query Embedding │         │ registry.json   │
 │ Text Cleaning   │         │ FAISS Search    │         │ metadata.json   │
 │ Fixed-size      │         │ Cross Encoder   │         │ Chunk Metadata  │
 │ Chunking        │         │ Prompt Builder  │         └─────────────────┘
 │ Embeddings      │         │ Groq LLM        │
 │ FAISS Index     │         │ Citations       │
 └─────────────────┘         └─────────────────┘
```

---

## Document Ingestion Pipeline

```text
PDF Upload
      │
      ▼
PDF Text Extraction
      │
      ▼
Text Cleaning
      │
      ▼
Fixed-size Sliding Window Chunking
(chunk_size + overlap)
      │
      ▼
Sentence Transformer Embeddings
      │
      ▼
FAISS Index
      │
      ▼
Save Chunk Metadata
(registry.json + metadata.json)
```

---

## Query Pipeline

```text
User Question
      │
      ▼
Query Embedding
      │
      ▼
FAISS Similarity Search
      │
      ▼
Top-20 Candidate Chunks
      │
      ▼
Cross-Encoder Reranker
      │
      ▼
Top-5 Relevant Chunks
      │
      ▼
Prompt Construction
      │
      ▼
Groq LLM
      │
      ▼
Grounded Answer
      │
      ▼
Source Citations
```

                        
              

## Tech Stack
- FastAPI — backend API
- Streamlit — frontend
- Sentence Transformers (all-MiniLM-L6-v2) — embeddings
- FAISS — vector index
- Cross-encoder (ms-marco-MiniLM-L-6-v2) — reranking
- Groq (Llama 3.3 70B) — generation

## Features
- Multi-document ingestion with duplicate detection
- Page-level citations with relevance scores
- Persistent FAISS index across restarts
- Measured retrieval quality (hit rate, MRR)

## Known Limitations
- FAISS index is local disk-based, not suited for distributed deployment
- Single retrieval failure mode identified: vocabulary mismatch between 
  query phrasing and document phrasing (e.g. "research questions" vs 
  literal "RQ1/RQ2" labels) — HyDE is the standard fix, not yet implemented
- No hybrid (keyword + semantic) retrieval — in progress on v2 branch
