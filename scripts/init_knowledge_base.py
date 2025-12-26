import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.document_loader import process_document
from utils.vectordb import get_collection, add_documents_to_collection

DOCS_DIR = os.path.join(os.getcwd(), "data", "sample_docs")

def init_knowledge_base():
    try:
        collection = get_collection()
    except ValueError as e:
        print(f"Error initializing ChromaDB client: {e}")
        return

    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
        print(f"Created directory: {DOCS_DIR}")
    
    # Get all PDF files
    files = [f for f in os.listdir(DOCS_DIR) if f.endswith(".pdf")]
    
    if not files:
        print(f"No PDF files found in {DOCS_DIR}.")
        return

    print(f"Found {len(files)} documents.")
    
    all_chunks = []
    all_metadatas = []
    all_ids = []
    
    for filename in files:
        file_path = os.path.join(DOCS_DIR, filename)
        print(f"Processing {filename}...")
        
        chunks = process_document(file_path)
        print(f"  - Generated {len(chunks)} chunks.")
        
        for i, chunk in enumerate(chunks):
            # Simple unique ID
            doc_id = f"{filename}_{i}"
            all_chunks.append(chunk)
            all_metadatas.append({"source": filename, "chunk_index": i})
            all_ids.append(doc_id)
            
    if all_chunks:
        print(f"Adding {len(all_chunks)} chunks to ChromaDB...")
        try:
            add_documents_to_collection(collection, all_chunks, all_metadatas, all_ids)
            print("Knowledge base initialized successfully!")
        except Exception as e:
            print(f"Error adding documents to ChromaDB: {e}")
    else:
        print("No content to add.")

if __name__ == "__main__":
    init_knowledge_base()
