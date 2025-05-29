import io
import PyPDF2
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document


def extract_text(file_bytes: bytes) -> str:
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
        text_pages = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_pages.append(page_text)
        return "\n".join(text_pages)
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {e}")
    
    
def extract_text_by_page(file_bytes: bytes, filename: str):
    reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    all_chunks = []
    for i, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if not page_text:
            continue
        chunks = splitter.split_text(page_text)
        for chunk in chunks:
            doc = Document(
                page_content=chunk,
                metadata={"source": filename, "page": i + 1}
            )
            all_chunks.append(doc)
    return all_chunks
