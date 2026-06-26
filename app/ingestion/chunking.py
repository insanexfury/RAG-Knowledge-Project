from app.core.config import settings

def chunk_pages(pages: list[dict]) -> list[dict]:
    chunked_pages = []
    for page in pages:
        text = page["text"]
        metadata = page["metadata"]
        chunks = chunk_text(text)
        for i, chunk in enumerate(chunks):
            chunked_pages.append({
                "text": chunk,
                "metadata": {
                    "page_number": metadata["page_number"],
                    "source": metadata["source"],
                    "chunk_index": i + 1 ,
                    "chunk_id": f"{metadata['source']}_p{metadata['page_number']}_c{i}"
                }
            })
    return chunked_pages

def chunk_text(text: str, chunk_size: int = None, chunk_overlap: int = None) -> list[str]:
    if chunk_size is None:
        chunk_size = settings.chunk_size
    if chunk_overlap is None:
        chunk_overlap = settings.chunk_overlap
    chunks = []
    for i in range(0, len(text), chunk_size - chunk_overlap):
        chunks.append(text[i:i + chunk_size])
    chunks = [c for c in chunks if len(c.strip()) >= 50]
    return chunks