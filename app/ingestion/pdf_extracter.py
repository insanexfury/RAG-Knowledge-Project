from pypdf import PdfReader
from pathlib import Path

def load_pdf(file_path: Path) -> list[dict]:
    """Load a PDF file and return a list of dictionaries containing page content."""
    if file_path.suffix.lower() == ".pdf" and file_path.exists():
        reader = PdfReader(file_path)
        pages = []
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                pages.append({"text": text,
                              "metadata": {
                                "page_number": page_num + 1,
                                "source": str(file_path.name)}
                            })
        return pages
    else:
        raise ValueError("Unsupported file format. Only PDF files are supported or file does not exist.")