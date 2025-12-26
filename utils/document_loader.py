import os
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_pdf(file_path):
    """
    Extracts text from a PDF file.
    
    Args:
        file_path (str): Path to the PDF file.
        
    Returns:
        str: Extracted text.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
        return text
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        return ""

def chunk_text(text, chunk_size=1000, chunk_overlap=200):
    """
    Splits text into chunks using RecursiveCharacterTextSplitter.
    
    Args:
        text (str): The text to split.
        chunk_size (int): Maximum size of each chunk.
        chunk_overlap (int): Overlap between chunks.
        
    Returns:
        list: List of text chunks.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    return splitter.split_text(text)

def process_document(file_path, chunk_size=1000, chunk_overlap=200):
    """
    Loads and chunks a document.
    
    Args:
        file_path (str): Path to the PDF file.
        chunk_size (int): Chunk size.
        chunk_overlap (int): Chunk overlap.
        
    Returns:
        list: List of text chunks.
    """
    text = load_pdf(file_path)
    if not text:
        return []
        
    chunks = chunk_text(text, chunk_size, chunk_overlap)
    return chunks
