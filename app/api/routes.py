from fastapi import APIRouter
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form ,Request
from app.api.schemas import (
    QueryRequest,
    QueryResponse,
    IngestResponse
)
from app.pipeline import RagPipeline
from app.citations.citation_formatter import format_citations
import os
import shutil
from contextlib import asynccontextmanager


router = APIRouter()
@router.post("/ingest",response_model=IngestResponse)
def ingest_file(file:UploadFile , request:Request):
    os.makedirs("temp",exist_ok=True)
    save_path=os.path.abspath(f"temp/{file.filename}")
    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    chunks = request.app.state.pipeline.ingest(Path(save_path))
    os.remove(save_path)
    return IngestResponse(filename = file.filename , chunks_indexed=chunks)

@router.post("/query",response_model=QueryResponse)
def query_req(question: QueryRequest,request:Request):
    result = request.app.state.pipeline.query(question.question)
    answer = result["answer"]
    retrieved_chunks = result["retrieved_chunks"]
    formatted_text = format_citations(retrieved_chunks)
    return QueryResponse(answer=answer,citations=formatted_text)

@router.get("/documents")
def list_documents(request: Request):
    return {"documents": list(request.app.state.pipeline.document_registry.keys())}