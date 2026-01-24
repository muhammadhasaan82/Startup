"""
Vector store manager using ChromaDB.
Handles storage and retrieval of document embeddings.
"""

import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional, Tuple
import logging

from config import config
from embeddings import embedding_manager

logger = logging.getLogger(__name__)


class VectorStore:
    """Manages ChromaDB vector storage and retrieval."""
    
    _instance = None
    _client = None
    _collection = None
    
    def __new__(cls):
        """Singleton pattern for vector store."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize ChromaDB client and collection."""
        if VectorStore._client is None:
            logger.info(f"Initializing ChromaDB at {config.CHROMA_PERSIST_DIR}")
            
            VectorStore._client = chromadb.PersistentClient(
                path=config.CHROMA_PERSIST_DIR,
                settings=Settings(anonymized_telemetry=False)
            )
            
            VectorStore._collection = VectorStore._client.get_or_create_collection(
                name=config.COLLECTION_NAME,
                metadata={"hnsw:space": "cosine"}
            )
            
            logger.info(f"Collection '{config.COLLECTION_NAME}' ready with {self.count()} documents")
    
    @property
    def collection(self):
        """Get the ChromaDB collection."""
        return VectorStore._collection
    
    def add_documents(self, documents: List[Dict[str, str]]) -> int:
        """
        Add documents to the vector store.
        
        Args:
            documents: List of dicts with 'content' and 'metadata' keys
            
        Returns:
            Number of documents added
        """
        if not documents:
            return 0
        
        # Extract content and metadata
        contents = [doc['content'] for doc in documents]
        metadatas = [doc.get('metadata', {}) for doc in documents]
        
        # Generate embeddings
        embeddings = embedding_manager.embed_texts(contents)
        
        # Generate unique IDs
        existing_count = self.count()
        ids = [f"doc_{existing_count + i}" for i in range(len(documents))]
        
        # Add to collection
        self.collection.add(
            embeddings=embeddings,
            documents=contents,
            metadatas=metadatas,
            ids=ids
        )
        
        logger.info(f"Added {len(documents)} documents to vector store")
        return len(documents)
    
    def search(
        self, 
        query: str, 
        n_results: int = None,
        distance_threshold: float = None
    ) -> List[Tuple[str, float, Dict]]:
        """
        Search for relevant documents.
        
        Args:
            query: Search query
            n_results: Maximum number of results (defaults to config.MAX_CONTEXT_DOCS)
            distance_threshold: Maximum distance for relevance (defaults to config.RELEVANCE_THRESHOLD)
            
        Returns:
            List of tuples: (content, distance, metadata)
        """
        n_results = n_results or config.MAX_CONTEXT_DOCS
        distance_threshold = distance_threshold or config.RELEVANCE_THRESHOLD
        
        if self.count() == 0:
            logger.warning("Vector store is empty")
            return []
        
        # Generate query embedding
        query_embedding = embedding_manager.embed_text(query)
        
        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=min(n_results, self.count()),
            include=["documents", "distances", "metadatas"]
        )
        
        # Process results
        processed = []
        
        if results['documents'] and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                distance = results['distances'][0][i] if results['distances'] else 0
                metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                
                # Filter by relevance threshold
                if distance <= distance_threshold:
                    processed.append((doc, distance, metadata))
        
        logger.info(f"Found {len(processed)} relevant documents for query")
        return processed
    
    def count(self) -> int:
        """Get the number of documents in the store."""
        return self.collection.count()
    
    def clear(self):
        """Clear all documents from the store."""
        # Delete and recreate collection
        VectorStore._client.delete_collection(config.COLLECTION_NAME)
        VectorStore._collection = VectorStore._client.create_collection(
            name=config.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        logger.info("Vector store cleared")
    
    def is_initialized(self) -> bool:
        """Check if the vector store has been populated with data."""
        return self.count() > 0


# Singleton instance
vector_store = VectorStore()
