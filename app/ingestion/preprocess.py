import re
def preprocess_pages(pages: list[dict]) -> list[dict]:
    """Preprocess the text content of each page."""
    cleaned_pages = []
    for page in pages:
        cleaned_page = page.copy()
        cleaned_page["text"] = preprocess_text(page["text"])
        cleaned_pages.append(cleaned_page)
    # drop pages with empty text after preprocessing
    cleaned_pages = [page for page in cleaned_pages if page["text"]]
    return cleaned_pages

def preprocess_text(text: str) -> str:
    """Preprocess the text by normalizing whitespace and removing unwanted characters."""
    # Remove Hyphenation at line breaks and repeated newlines
    text = re.sub(r"-\n", "", text)
    text = re.sub(r"\n+", "\n", text)
    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text).strip()
    # Remove unwanted characters (e.g., non-printable characters)
    text = "".join(c for c in text if c.isprintable())
    return text