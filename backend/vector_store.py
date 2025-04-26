import os
import pinecone
import numpy as np
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional
import json
import openai

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class VectorStore:
    def __init__(self):
        self.index = None
        self.namespace = "legal-documents"
        self.connect()
    
    def connect(self):
        """Connect to Pinecone"""
        try:
            # Initialize Pinecone
            pinecone_api_key = os.getenv("PINECONE_API_KEY")
            pinecone_environment = os.getenv("PINECONE_ENVIRONMENT", "gcp-starter")
            
            if pinecone_api_key:
                pinecone.init(
                    api_key=pinecone_api_key,
                    environment=pinecone_environment
                )
                
                # Check if index exists, if not create it
                index_name = "legal-documents"
                
                # List existing indexes
                existing_indexes = pinecone.list_indexes()
                
                # Create index if it doesn't exist
                if index_name not in existing_indexes:
                    pinecone.create_index(
                        name=index_name,
                        dimension=1536,  # OpenAI embedding dimension
                        metric="cosine"
                    )
                    print(f"Created new Pinecone index: {index_name}")
                
                # Connect to the index
                self.index = pinecone.Index(index_name)
                print("Connected to Pinecone index")
            else:
                # Fallback to in-memory storage
                print("Pinecone API key not found, using in-memory storage")
                self.index = None
                self.stored_vectors = {}  # In-memory fallback
        except Exception as e:
            print(f"Error connecting to Pinecone: {e}")
            # Fallback to in-memory storage
            self.index = None
            self.stored_vectors = {}
    
    def embed_text(self, text: str) -> List[float]:
        """Generate embedding using OpenAI API"""
        try:
            response = openai.Embedding.create(
                model="text-embedding-ada-002",
                input=text[:8191]  # OpenAI has a token limit
            )
            return response["data"][0]["embedding"]
        except Exception as e:
            print(f"Error generating OpenAI embedding: {e}")
            # Simple fallback embedding method
            embedding = []
            for i in range(1536):  # Match OpenAI embedding dimension
                val = sum([(ord(c) * (i + 1)) % 256 for c in text[:100]]) / 256.0
                embedding.append(val)
            return embedding
    
    def add_document(self, document_id: str, title: str, chunks: List[str], 
                    clause_types: Optional[List[str]] = None) -> bool:
        """Add document chunks to Pinecone"""
        if not clause_types:
            clause_types = [None] * len(chunks)
        
        try:
            # If using Pinecone
            if self.index:
                vectors_to_upsert = []
                
                for i, chunk in enumerate(chunks):
                    # Generate embedding
                    embedding = self.embed_text(chunk)
                    
                    # Create metadata
                    metadata = {
                        "content": chunk[:1000],  # Limit metadata size
                        "document_id": document_id,
                        "chunk_id": i,
                        "title": title
                    }
                    
                    if i < len(clause_types) and clause_types[i]:
                        metadata["clause_type"] = clause_types[i]
                    
                    # Create vector ID
                    vector_id = f"{document_id}_chunk_{i}"
                    
                    # Add to upsert list
                    vectors_to_upsert.append({
                        "id": vector_id,
                        "values": embedding,
                        "metadata": metadata
                    })
                
                # Upsert in batches (Pinecone has size limits)
                batch_size = 100
                for i in range(0, len(vectors_to_upsert), batch_size):
                    batch = vectors_to_upsert[i:i+batch_size]
                    self.index.upsert(vectors=batch, namespace=self.namespace)
                
                return True
            
            # Fallback to in-memory storage
            else:
                for i, chunk in enumerate(chunks):
                    embedding = self.embed_text(chunk)
                    vector_id = f"{document_id}_chunk_{i}"
                    
                    self.stored_vectors[vector_id] = {
                        "content": chunk,
                        "document_id": document_id,
                        "chunk_id": i,
                        "title": title,
                        "embedding": embedding,
                        "clause_type": clause_types[i] if i < len(clause_types) else None
                    }
                return True
                
        except Exception as e:
            print(f"Error adding document to vector store: {e}")
            return False
    
    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant document chunks"""
        try:
            # Generate query embedding
            query_embedding = self.embed_text(query)
            
            # If using Pinecone
            if self.index:
                search_response = self.index.query(
                    namespace=self.namespace,
                    vector=query_embedding,
                    top_k=limit,
                    include_metadata=True
                )
                
                results = []
                for match in search_response.matches:
                    results.append({
                        "content": match.metadata["content"],
                        "document_id": match.metadata["document_id"],
                        "title": match.metadata["title"],
                        "chunk_id": match.metadata["chunk_id"],
                        "clause_type": match.metadata.get("clause_type")
                    })
                
                return results
            
            # Fallback to in-memory search
            else:
                if not self.stored_vectors:
                    return []
                
                results = []
                for vector_id, data in self.stored_vectors.items():
                    embedding = data["embedding"]
                    # Calculate cosine similarity
                    similarity = np.dot(query_embedding, embedding) / (
                        np.linalg.norm(query_embedding) * np.linalg.norm(embedding)
                    )
                    results.append((data, similarity))
                
                # Sort by similarity and get top results
                results.sort(key=lambda x: x[1], reverse=True)
                top_results = results[:limit]
                
                return [{
                    "content": data["content"],
                    "document_id": data["document_id"],
                    "title": data["title"],
                    "chunk_id": data["chunk_id"],
                    "clause_type": data["clause_type"]
                } for data, _ in top_results]
                
        except Exception as e:
            print(f"Error searching in vector store: {e}")
            return []