
import sqlite3
import json
import hashlib
import os
from datetime import datetime, timedelta

CACHE_DB_PATH = os.path.join(os.getcwd(), "data", "cache.db")

def init_cache():
    """Initializes the SQLite cache database."""
    os.makedirs(os.path.dirname(CACHE_DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(CACHE_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_cache (
            query_hash TEXT PRIMARY KEY,
            query_text TEXT,
            results JSON,
            timestamp DATETIME,
            expires_at DATETIME
        )
    """)
    
    conn.commit()
    conn.close()

def get_query_hash(query: str) -> str:
    """Returns MD5 hash of the query."""
    return hashlib.md5(query.strip().lower().encode()).hexdigest()

def get_cached_results(query: str):
    """
    Retrieves cached results for a query if they exist and haven't expired.
    """
    query_hash = get_query_hash(query)
    
    conn = sqlite3.connect(CACHE_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT results, expires_at FROM search_cache WHERE query_hash = ?", 
        (query_hash,)
    )
    row = cursor.fetchone()
    conn.close()
    
    if row:
        results_json, expires_at_str = row
        expires_at = datetime.fromisoformat(expires_at_str)
        
        if datetime.now() < expires_at:
            # Cache hit
            return json.loads(results_json)
        else:
            # Cache expired
            return None
            
    return None

def save_to_cache(query: str, results: list, ttl_hours: int = 24):
    """
    Saves search results to the cache.
    """
    if not results:
        return

    query_hash = get_query_hash(query)
    expires_at = datetime.now() + timedelta(hours=ttl_hours)
    
    conn = sqlite3.connect(CACHE_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT OR REPLACE INTO search_cache (query_hash, query_text, results, timestamp, expires_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        query_hash, 
        query, 
        json.dumps(results), 
        datetime.now().isoformat(), 
        expires_at.isoformat()
    ))
    
    conn.commit()
    conn.close()
