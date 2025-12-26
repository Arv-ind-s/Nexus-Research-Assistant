import os
import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()

# Define persistence directory
PERSIST_DIRECTORY = os.path.join(os.getcwd(), "data", "chroma_db")

def get_chroma_client():
    """Returns a persistent ChromaDB client."""
    return chromadb.PersistentClient(path=PERSIST_DIRECTORY)

def get_embedding_function():
    """Returns the OpenAI embedding function."""
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables.")
    
    return embedding_functions.OpenAIEmbeddingFunction(
        api_key=openai_api_key,
        model_name="text-embedding-3-small"
    )

def get_collection(name="nexus_knowledge_base"):
    """Gets or creates the vector database collection."""
    client = get_chroma_client()
    embedding_fn = get_embedding_function()
    return client.get_or_create_collection(
        name=name,
        embedding_function=embedding_fn
    )

def add_documents_to_collection(collection, documents, metadatas, ids):
    """
    Adds documents to the collection.
    
    Args:
        collection: The ChromaDB collection object.
        documents (list): List of text strings.
        metadatas (list): List of metadata dicts.
        ids (list): List of unique IDs.
    """
    collection.add(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )

def search_collection(collection, query_texts, n_results=5):
    """
    Queries the collection.
    
    Args:
        collection: The ChromaDB collection object.
        query_texts (list): List of query strings (usually just one).
        n_results (int): Number of results to return.
        
    Returns:
        dict: Query results.
    """
    return collection.query(
        query_texts=query_texts,
        n_results=n_results
    )
