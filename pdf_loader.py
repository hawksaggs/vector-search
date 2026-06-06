from pypdf import PdfReader

def load_pdf(file_path):
    """
    Loads a PDF file and extracts its text content.
    Returns a list of dictionaries with 'title' and 'content' keys.
    """
    reader = PdfReader(file_path)
    documents = []
    
    for page in reader.pages:
        text = page.extract_text()
        if text:
            documents.append({
                "title": f"{file_path} - Page {reader.pages.index(page) + 1}",
                "content": text
            })
    
    return documents

def extract_text_from_pdf(file_path):
    """
    Loads a PDF file and extracts its text content as a single string.
    """
    reader = PdfReader(file_path)
    full_text = ""
    
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"
    
    return full_text.strip()

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """
     Splits text into overlapping chunks using a sliding window.

    chunk_size : characters per chunk
    overlap    : characters shared between consecutive chunks

    The window slides forward by (chunk_size - overlap) each step.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap  # Move start forward by chunk_size minus overlap
    return chunks   

pdf_text = extract_text_from_pdf("engineering_handbook.pdf")
chunked_texts = chunk_text(pdf_text, chunk_size=500, overlap=50)
print("\n\n".join(chunked_texts))