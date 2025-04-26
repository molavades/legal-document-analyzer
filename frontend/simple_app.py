import streamlit as st

st.set_page_config(page_title="Legal Document Analyzer", page_icon="⚖️", layout="wide")

# Header
st.title("⚖️ Legal Document Analysis System")
st.markdown("A tool for legal professionals to analyze contracts and legal documents")

# Project Overview
st.markdown("""
## Project Overview

This system enables legal professionals to:
* Extract key clauses and entities from legal documents
* Compare clauses across different documents
* Generate plain-language summaries
* Identify potential legal risks
""")

# Features
st.markdown("""
## Key Features

* **Document Processing**: Supports PDF and text formats
* **Entity Extraction**: Identifies parties, dates, monetary values, and obligations
* **Clause Detection**: Automatically identifies important clause types
* **Semantic Search**: Find relevant content across all documents
* **Risk Assessment**: AI-powered identification of potential issues
* **Document Comparison**: Side-by-side analysis of differences
""")

# Technology
st.markdown("""
## Technology Stack

* **Backend**: FastAPI for document processing and analysis
* **Frontend**: Streamlit for intuitive user interface
* **Vector Storage**: For efficient semantic retrieval
* **LLM Integration**: OpenAI GPT-4o for legal understanding
* **Dataset**: Based on CUAD (Contract Understanding Atticus Dataset)
""")

# Demo Images
st.markdown("## Screenshots")
st.markdown("### Document Analysis")
st.image("https://raw.githubusercontent.com/user-attachments/assets/main/31d801ad-6f63-4788-b667-f44a7bcc3c23")

st.markdown("### Sample extracted clauses")
st.code("""
Governing Law: This Agreement is governed by the laws of the State of Delaware.

Termination: Either party may terminate this Agreement with 30 days written notice.

Confidentiality: Each party shall maintain the confidentiality of all proprietary information.
""")

# GitHub Repository
st.markdown("""
## GitHub Repository

The complete code with full functionality is available in the [GitHub repository](https://github.com/molavades/legal-document-analyzer).

The repository includes:
* FastAPI backend with document processing
* CUAD dataset integration
* Vector-based semantic search
* Legal entity and clause extraction
* Document comparison functionality
""")
