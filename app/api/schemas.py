from pydantic import BaseModel
class QueryRequest(BaseModel):
    question:str 
class QueryResponse(BaseModel):
    answer:str
    citations:list[dict]
class IngestResponse(BaseModel):
    filename:str
    chunks_indexed:int