# Legal Document Analysis System

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.103.1-teal.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.26.0-red.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-purple.svg)
![Pinecone](https://img.shields.io/badge/Pinecone-2.2.2-orange.svg)

A legal document analysis system that leverages generative AI and vector databases to facilitate contract review, risk assessment, and insight extraction from legal documents.

## 📚 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Challenges and Solutions](#challenges-and-solutions)
- [Future Enhancements](#future-enhancements)
- [References](#references)

## 🔍 Overview

The Legal Document Analysis System is designed to assist legal professionals in efficiently analyzing and extracting insights from contracts and legal documents. By leveraging a combination of Retrieval Augmented Generation (RAG), vector database technology, and domain-specific legal knowledge, the system automates time-consuming aspects of contract review.

The system is built on the Contract Understanding Atticus Dataset (CUAD), which contains 510 commercial legal contracts with over 13,000 expert annotations spanning 41 categories of important legal clauses.

## ✨ Features

- **Document Processing**: Extract text from PDF and TXT files with intelligent chunking
- **Entity Extraction**: Identify parties, dates, monetary values, and other key entities
- **Clause Identification**: Automatically detect 41 types of legal clauses (governing law, termination, etc.)
- **Plain Language Summaries**: Generate concise, readable summaries of complex legal text
- **Risk Assessment**: Evaluate potential risks in contracts with severity ratings
- **Document Comparison**: Compare similar clauses across multiple contracts to identify discrepancies
- **Semantic Search**: Find relevant information across documents using natural language queries

## 📂 Project Structure

```
legal-document-analyzer/
├── backend/                    # FastAPI backend services
│   ├── app.py                  # Main API endpoints
│   ├── document_processor.py   # Document parsing logic
│   ├── vector_store.py         # Pinecone integration
│   ├── legal_analysis.py       # Legal analysis with OpenAI
│   ├── download_cuad.py        # Script to download CUAD dataset
│   └── requirements.txt        # Backend dependencies
├── frontend/                   # Streamlit UI
│   ├── app.py                  # Main UI application
│   └── requirements.txt        # Frontend dependencies
├── data/                       # Storage for CUAD dataset
├── docker-compose.yml          # Docker configuration
├── streamlit_app.py            # Combined app for deployment
├── .env                        # Environment variables
├── requirements.txt            # Combined requirements
└── README.md                   # Project documentation
```

#
# Legal Document Analysis System

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10-green.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.103.1-teal.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.26.0-red.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-purple.svg)
![Pinecone](https://img.shields.io/badge/Pinecone-2.2.2-orange.svg)

A sophisticated legal document analysis system that leverages AI and natural language processing to streamline contract review, risk assessment, and insight extraction from legal documents.

## 📚 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Challenges and Solutions](#challenges-and-solutions)
- [Future Enhancements](#future-enhancements)
- [Contact](#contact)

## 🔍 Overview

The Legal Document Analysis System is designed to help legal professionals efficiently analyze and extract insights from contracts and legal documents. By combining advanced text processing techniques with domain-specific legal knowledge, the system automates time-consuming aspects of contract review, enabling lawyers to focus on higher-value tasks.

The system is built using the Contract Understanding Atticus Dataset (CUAD), which contains 510 commercial legal contracts with over 13,000 expert annotations spanning 41 categories of important legal clauses.

## ✨ Features

- **Document Processing**: Extract text from PDF and TXT files with intelligent chunking
- **Entity Extraction**: Identify parties, dates, monetary values, and locations within contracts
- **Clause Identification**: Automatically detect and categorize different types of legal clauses
- **Risk Assessment**: Evaluate potential risks in contracts with severity ratings
- **Document Comparison**: Compare similar clauses across multiple documents to identify discrepancies
- **Semantic Search**: Find relevant information across documents using natural language queries
- **Interactive Visualization**: Explore document analysis through an intuitive user interface

## 🏗️ System Architecture

---
┌─────────────────┐         ┌──────────────────┐         ┌────────────────┐
│                 │         │                  │         │                │
│    Streamlit    │ ◄─────► │     FastAPI      │ ◄─────► │    Pinecone    │
│    Frontend     │         │     Backend      │         │  Vector Store  │
│                 │         │                  │         │                │
└─────────────────┘         └──────────────────┘         └────────────────┘
                                     ▲
                                     │
                                     ▼
                            ┌──────────────────┐
                            │                  │
                            │    OpenAI API    │
                            │                  │
                            └──────────────────┘
---

The system follows a three-tier architecture:

1. **Presentation Layer** (Streamlit Frontend):
   - User interface for document upload and interaction
   - Results visualization and document comparison tools

2. **Business Logic Layer** (FastAPI Backend):
   - Document processing and chunking
   - Entity and clause extraction
   - Integration with OpenAI for embeddings and analysis
   - API endpoints for frontend communication

3. **Data Layer** (Pinecone Vector Database):
   - Storage of document chunks as vectors
   - Semantic search capabilities
   - Metadata management for document retrieval

## 🛠️ Installation

### Prerequisites

- Python 3.10+
- OpenAI API key
- Pinecone API key

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/legal-document-analyzer.git
   cd legal-document-analyzer
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_api_key
   PINECONE_API_KEY=your_pinecone_api_key
   PINECONE_ENVIRONMENT=your_pinecone_environment
   ```

5. Download the CUAD dataset:
   ```bash
   cd backend
   python download_cuad.py
   cd ..
   ```

## 🚀 Usage

### Running Locally

1. Start the backend server:
   ```bash
   cd backend
   uvicorn app:app --reload
   ```

2. In a new terminal, start the frontend:
   ```bash
   cd frontend
   streamlit run app.py
   ```

3. Open your browser and navigate to http://localhost:8501

### Using the Application

1. **Upload Documents**:
   - Go to the "Upload Document" tab
   - Select a PDF or TXT file
   - Click "Process Document"

2. **View Documents**:
   - Navigate to the "View Documents" tab
   - Select a document from the list
   - Explore different views: Overview, Entities, Clauses, Summary, Risk Assessment

3. **Compare Documents**:
   - Go to the "Compare Documents" tab
   - Select two documents to compare
   - View differences in key clauses and provisions

4. **Search Documents**:
   - Navigate to the "Search" tab
   - Enter a natural language query
   - Review relevant sections from across all documents

### Deployment

For deployment on Streamlit Cloud:

1. Push the code to a GitHub repository
2. Sign up for Streamlit Cloud at https://streamlit.io/cloud
3. Connect your GitHub repository
4. Set the main file path to `streamlit_app.py`
5. Add your API keys under Advanced Settings

## 💻 Technologies Used

- **Python 3.10**: Core programming language
- **FastAPI**: Backend API framework
- **Streamlit**: Frontend user interface
- **OpenAI API**: Embeddings and analysis
- **Pinecone**: Vector database for document storage
- **PyPDF2**: PDF processing
- **NumPy**: Numerical computations
- **CUAD Dataset**: Domain-specific legal data

## 🧩 Challenges and Solutions

### Challenge 1: Legal Context Understanding
Even advanced LLMs sometimes struggle with the nuanced language in legal documents. 

**Solution**: Carefully engineered prompts with specific instructions for legal interpretation and context preservation.

### Challenge 2: Balancing Precision and Recall
When identifying clauses, there's a tradeoff between finding all relevant clauses (recall) and avoiding false positives (precision).

**Solution**: Tuned the system to prioritize recall since missing important clauses poses a greater risk in legal contexts.

### Challenge 3: API Rate Limits
Working with external APIs for embeddings and completions meant dealing with rate limits and costs.

**Solution**: Implemented caching, batching of requests, and fallback mechanisms to optimize API usage.

### Challenge 4: Vector Database Integration
Connecting to Pinecone required handling connection issues in a robust way.

**Solution**: Created a flexible architecture with in-memory fallback storage when Pinecone is unavailable.

## 🔮 Future Enhancements

- **Multi-language Support**: Add capabilities for analyzing contracts in different languages
- **Custom Model Fine-tuning**: Train specialized models on legal text for improved performance
- **Document History Tracking**: Implement version comparison for document revisions
- **Integration with Legal Research Databases**: Connect with external legal resources
- **Collaborative Features**: Add multi-user annotation and commenting capabilities

## 📚 References

1. Contract Understanding Atticus Dataset (CUAD): https://www.atticusprojectai.org/cuad
2. Hendrycks, D., Burns, C., Chen, A., & Ball, S. (2021). CUAD: An Expert-Annotated NLP Dataset for Legal Contract Review. NeurIPS.
3. Pinecone Vector Database: https://www.pinecone.io/
4. OpenAI API Documentation: https://platform.openai.com/docs/
5. FastAPI Documentation: https://fastapi.tiangolo.com/
6. Streamlit Documentation: https://docs.streamlit.io/
7. PyPDF2 Documentation: https://pypdf2.readthedocs.io/
8. Retrieval Augmented Generation (RAG) Patterns: https://www.pinecone.io/learn/retrieval-augmented-generation/
