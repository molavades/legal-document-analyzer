# backend/app.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import uuid
from typing import List, Optional
import json
import os
from document_processor import LegalDocumentProcessor
from vector_store import VectorStore
from legal_analysis import LegalAnalyzer  # Add this line
app = FastAPI(title="Legal Document Analysis API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize document processor and vector store
document_processor = LegalDocumentProcessor()
vector_store = VectorStore()

# In-memory document storage (replace with database in production)
documents = {}

@app.get("/")
def read_root():
    return {"message": "Legal Document Analysis API"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a legal document"""
    try:
        # Generate unique ID for document
        document_id = str(uuid.uuid4())
        
        # Read file content
        file_content = await file.read()
        
        # Process document based on file type
        if file.filename.lower().endswith('.pdf'):
            text = document_processor.extract_text_from_pdf(file_content)
        elif file.filename.lower().endswith('.txt'):
            text = document_processor.extract_text_from_txt(file_content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Only PDF and TXT files are supported.")
        
        # Split text into chunks
        chunks = document_processor.chunk_document(text)
        
        # Extract legal entities
        entities = document_processor.extract_legal_entities(text)
        
        # Identify clause types
        clauses = document_processor.identify_clause_types(text)
        
        # Store document in memory
        documents[document_id] = {
            "id": document_id,
            "filename": file.filename,
            "text": text,
            "entities": entities,
            "clauses": {k: [item[1] for item in v] for k, v in clauses.items()},
            "clause_summaries": {k: [item[0] for item in v] for k, v in clauses.items()}
        }
        
        # Store in vector database
        clause_types = []
        for chunk in chunks:
            # Find most relevant clause type for this chunk
            chunk_clause_type = None
            for clause_type, clause_paragraphs in clauses.items():
                for _, full_clause in clause_paragraphs:
                    if full_clause in chunk:
                        chunk_clause_type = clause_type
                        break
                if chunk_clause_type:
                    break
            clause_types.append(chunk_clause_type)
        
        vector_store.add_document(document_id, file.filename, chunks, clause_types)
        
        # Return basic document information
        return {
            "document_id": document_id,
            "filename": file.filename,
            "content_preview": text[:200] + "..." if len(text) > 200 else text,
            "num_chunks": len(chunks),
            "entities": entities,
            "clause_summaries": {k: [item[0] for item in v] for k, v in clauses.items()}
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
def get_documents():
    """Get list of all uploaded documents"""
    result = []
    for doc_id, doc in documents.items():
        result.append({
            "id": doc_id,
            "filename": doc["filename"],
            "preview": doc["text"][:200] + "..." if len(doc["text"]) > 200 else doc["text"]
        })
    return result

@app.get("/documents/{document_id}")
def get_document(document_id: str):
    """Get document details by ID"""
    if document_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")
    
    doc = documents[document_id]
    return {
        "id": doc["id"],
        "filename": doc["filename"],
        "text": doc["text"],
        "entities": doc["entities"],
        "clauses": doc["clause_summaries"]
    }

@app.post("/search")
def search_documents(query: str = Form(...)):
    """Search for content across documents"""
    results = vector_store.search(query)
    return results

@app.get("/clauses/{document_id}")
def get_document_clauses(document_id: str):
    """Get all identified clauses for a document"""
    if document_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")
    
    doc = documents[document_id]
    return doc["clause_summaries"]

# Updated endpoints to add to backend/app.py

@app.post("/summarize/{document_id}")
def summarize_document(document_id: str):
    """Generate a plain language summary of a document"""
    if document_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Initialize legal analyzer
    analyzer = LegalAnalyzer()
    
    # Generate summary
    doc = documents[document_id]
    summary = analyzer.generate_summary(doc["text"])
    
    return {"summary": summary}

@app.post("/risk-assessment/{document_id}")
def assess_risks(document_id: str):
    """Identify potential risks in a document"""
    if document_id not in documents:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Initialize legal analyzer
    analyzer = LegalAnalyzer()
    
    # Generate risk assessment
    doc = documents[document_id]
    risks = analyzer.identify_risks(doc["text"])
    
    return {"risks": risks}

@app.post("/compare")
def compare_documents(doc1_id: str = Form(...), doc2_id: str = Form(...)):
    """Compare two documents and identify differences"""
    if doc1_id not in documents:
        raise HTTPException(status_code=404, detail="First document not found")
    if doc2_id not in documents:
        raise HTTPException(status_code=404, detail="Second document not found")
    
    # Initialize legal analyzer
    analyzer = LegalAnalyzer()
    
    # Compare documents
    doc1 = documents[doc1_id]
    doc2 = documents[doc2_id]
    comparison = analyzer.compare_documents(doc1["text"], doc2["text"])
    
    return comparison

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)