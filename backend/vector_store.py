# backend/vector_store.py
import numpy as np
from typing import List, Dict, Any, Optional

class VectorStore:
    def __init__(self):
        self.documents = []  # Store documents in memory
    
    def connect(self):
        """Dummy connect method"""
        print("Using in-memory vector storage")
    
    def setup_schema(self):
        """Dummy schema setup"""
        pass
    
    def embed_text(self, text: str) -> List[float]:
        """Generate a simple embedding for text"""
        # Simple embedding method that uses character frequencies
        chars = set(text.lower())
        embedding = []
        for i in range(384):
            val = sum([(ord(c) * (i + 1)) % 256 for c in text]) / 256.0
            embedding.append(val)
        return embedding
    
    def add_document(self, document_id: str, title: str, chunks: List[str], 
                    clause_types: Optional[List[str]] = None) -> bool:
        """Add document chunks to the vector store"""
        if not clause_types:
            clause_types = [None] * len(chunks)
        
        try:
            for i, chunk in enumerate(chunks):
                embedding = self.embed_text(chunk)
                document = {
                    "content": chunk,
                    "document_id": document_id,
                    "chunk_id": i,
                    "title": title,
                    "embedding": embedding,
                    "clause_type": clause_types[i] if i < len(clause_types) else None
                }
                self.documents.append(document)
            return True
        except Exception as e:
            print(f"Error adding document to vector store: {e}")
            return False
    
    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant document chunks using cosine similarity"""
        if not self.documents:
            return []
            
        try:
            query_embedding = self.embed_text(query)
            
            # Calculate cosine similarity with all documents
            results = []
            for doc in self.documents:
                embedding = doc["embedding"]
                # Cosine similarity calculation
                similarity = np.dot(query_embedding, embedding) / (
                    np.linalg.norm(query_embedding) * np.linalg.norm(embedding)
                )
                results.append((doc, similarity))
            
            # Sort by similarity and get top results
            results.sort(key=lambda x: x[1], reverse=True)
            top_results = results[:limit]
            
            # Format results
            return [{
                "content": doc["content"],
                "document_id": doc["document_id"],
                "title": doc["title"],
                "chunk_id": doc["chunk_id"],
                "clause_type": doc["clause_type"] if "clause_type" in doc else None
            } for doc, _ in top_results]
        except Exception as e:
            print(f"Error searching in vector store: {e}")
            return []