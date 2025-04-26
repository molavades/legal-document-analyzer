# frontend/app.py
import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API URL
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="Legal Document Analyzer",
    page_icon="⚖️",
    layout="wide"
)

# Initialize session state
if 'uploaded_documents' not in st.session_state:
    st.session_state.uploaded_documents = []
if 'selected_document' not in st.session_state:
    st.session_state.selected_document = None
if 'tab' not in st.session_state:
    st.session_state.tab = "upload"

# Function to fetch documents from API
def get_documents():
    try:
        response = requests.get(f"{API_URL}/documents")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching documents: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return []

# Function to upload document
def upload_document(file):
    try:
        files = {"file": (file.name, file.getvalue(), file.type)}
        response = requests.post(f"{API_URL}/upload", files=files)
        if response.status_code == 200:
            st.session_state.uploaded_documents = get_documents()
            return response.json()
        else:
            st.error(f"Error uploading document: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return None

# Function to get document details
def get_document_details(doc_id):
    try:
        response = requests.get(f"{API_URL}/documents/{doc_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching document details: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return None

# Function to get document clauses
def get_document_clauses(doc_id):
    try:
        response = requests.get(f"{API_URL}/clauses/{doc_id}")
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching document clauses: {response.text}")
            return {}
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return {}

# Function to generate document summary
def summarize_document(doc_id):
    try:
        response = requests.post(f"{API_URL}/summarize/{doc_id}")
        if response.status_code == 200:
            return response.json()["summary"]
        else:
            st.error(f"Error generating summary: {response.text}")
            return "Error generating summary"
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return "Error connecting to API"

# Function to assess document risks
def assess_document_risks(doc_id):
    try:
        response = requests.post(f"{API_URL}/risk-assessment/{doc_id}")
        if response.status_code == 200:
            return response.json()["risks"]
        else:
            st.error(f"Error assessing risks: {response.text}")
            return []
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return []

# Function to compare documents
def compare_documents(doc1_id, doc2_id):
    try:
        response = requests.post(
            f"{API_URL}/compare",
            data={"doc1_id": doc1_id, "doc2_id": doc2_id}
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error comparing documents: {response.text}")
            return {"error": "Error comparing documents"}
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
        return {"error": f"Error connecting to API: {e}"}

# Header
st.title("⚖️ Legal Document Analyzer")
st.markdown("A tool for legal professionals to analyze contracts and legal documents")

# Sidebar with navigation
st.sidebar.title("Navigation")
tab = st.sidebar.radio(
    "Choose a tab",
    ["Upload Document", "View Documents", "Compare Documents", "Search"]
)
st.session_state.tab = tab.lower().replace(" ", "_")

# Load documents
if st.session_state.tab != "upload_document":
    st.session_state.uploaded_documents = get_documents()

# Upload Document Tab
if st.session_state.tab == "upload_document":
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF or TXT file", type=["pdf", "txt"])
    
    if uploaded_file:
        st.write("File details:")
        st.write(f"- Name: {uploaded_file.name}")
        st.write(f"- Type: {uploaded_file.type}")
        st.write(f"- Size: {round(len(uploaded_file.getvalue()) / 1024, 2)} KB")
        
        if st.button("Process Document"):
            with st.spinner("Processing document..."):
                result = upload_document(uploaded_file)
                if result:
                    st.success("Document uploaded and processed successfully!")
                    st.json(result)

# View Documents Tab
elif st.session_state.tab == "view_documents":
    st.header("View Documents")
    
    if not st.session_state.uploaded_documents:
        st.info("No documents found. Please upload a document first.")
    else:
        # Create columns for document selection
        col1, col2 = st.columns([1, 3])
        
        with col1:
            st.subheader("Documents")
            for doc in st.session_state.uploaded_documents:
                if st.button(doc["filename"], key=f"btn_{doc['id']}"):
                    st.session_state.selected_document = doc["id"]
        
        with col2:
            if st.session_state.selected_document:
                doc_details = get_document_details(st.session_state.selected_document)
                if doc_details:
                    st.subheader(f"Document: {doc_details['filename']}")
                    
                    # Create tabs for different views
                    doc_tabs = st.tabs(["Overview", "Entities", "Clauses", "Summary", "Risk Assessment"])
                    
                    # Overview Tab
                    with doc_tabs[0]:
                        st.text_area("Document Content", doc_details["text"], height=400)
                    
                    # Entities Tab
                    with doc_tabs[1]:
                        st.subheader("Extracted Entities")
                        for entity_type, entities in doc_details["entities"].items():
                            if entities:
                                st.write(f"**{entity_type.capitalize()}:**")
                                for entity in entities[:10]:  # Limit to first 10
                                    st.write(f"- {entity}")
                    
                    # Clauses Tab
                    with doc_tabs[2]:
                        st.subheader("Identified Clauses")
                        clauses = doc_details["clauses"]
                        if clauses:
                            for clause_type, clause_texts in clauses.items():
                                if clause_texts:
                                    with st.expander(f"{clause_type.replace('_', ' ').title()} ({len(clause_texts)})"):
                                        for i, clause in enumerate(clause_texts):
                                            st.text_area(f"Clause {i+1}", clause, height=100, key=f"clause_{clause_type}_{i}")
                        else:
                            st.info("No clauses identified in this document.")
                    
                    # Summary Tab
                    with doc_tabs[3]:
                        st.subheader("Document Summary")
                        if st.button("Generate Summary"):
                            with st.spinner("Generating summary..."):
                                summary = summarize_document(st.session_state.selected_document)
                                st.write(summary)
                    
                    # Risk Assessment Tab
                    with doc_tabs[4]:
                        st.subheader("Risk Assessment")
                        if st.button("Assess Risks"):
                            with st.spinner("Analyzing risks..."):
                                risks = assess_document_risks(st.session_state.selected_document)
                                if risks:
                                    for risk in risks:
                                        severity_color = {
                                            "High": "red",
                                            "Medium": "orange",
                                            "Low": "green"
                                        }.get(risk.get("severity", "Unknown"), "gray")
                                        
                                        st.markdown(f"### {risk.get('description')}")
                                        st.markdown(f"**Severity:** :{severity_color}[{risk.get('severity')}]")
                                        st.markdown(f"**Clause:** {risk.get('clause')}")
                                        st.markdown("---")
                                else:
                                    st.info("No risks identified or error in risk assessment.")
            else:
                st.info("Select a document from the list to view details")

# Compare Documents Tab
elif st.session_state.tab == "compare_documents":
    st.header("Compare Documents")
    
    if len(st.session_state.uploaded_documents) < 2:
        st.info("You need at least two documents to use the comparison feature. Please upload more documents.")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("First Document")
            doc1_options = {doc["id"]: doc["filename"] for doc in st.session_state.uploaded_documents}
            doc1_id = st.selectbox("Select first document", options=list(doc1_options.keys()), format_func=lambda x: doc1_options[x])
        
        with col2:
            st.subheader("Second Document")
            doc2_options = {doc["id"]: doc["filename"] for doc in st.session_state.uploaded_documents if doc["id"] != doc1_id}
            doc2_id = st.selectbox("Select second document", options=list(doc2_options.keys()), format_func=lambda x: doc2_options[x])
        
        if st.button("Compare Documents"):
            with st.spinner("Comparing documents..."):
                comparison = compare_documents(doc1_id, doc2_id)
                if "error" not in comparison:
                    st.subheader("Comparison Results")
                    for category, details in comparison.items():
                        with st.expander(category.replace("_", " ").title()):
                            if isinstance(details, list):
                                for item in details:
                                    st.write(f"- {item}")
                            elif isinstance(details, dict):
                                for key, value in details.items():
                                    st.write(f"**{key}:** {value}")
                            else:
                                st.write(details)
                else:
                    st.error(comparison["error"])

# Search Tab
elif st.session_state.tab == "search":
    st.header("Search Documents")
    
    query = st.text_input("Enter your search query")
    
    if query and st.button("Search"):
        with st.spinner("Searching..."):
            try:
                response = requests.post(f"{API_URL}/search", data={"query": query})
                if response.status_code == 200:
                    results = response.json()
                    if results:
                        st.subheader("Search Results")
                        for i, result in enumerate(results):
                            with st.expander(f"Result {i+1} from {result['title']}"):
                                st.write(result["content"])
                                st.write(f"Document: {result['title']}")
                                if "clause_type" in result and result["clause_type"]:
                                    st.write(f"Clause Type: {result['clause_type']}")
                    else:
                        st.info("No results found for your query.")
                else:
                    st.error(f"Error searching: {response.text}")
            except Exception as e:
                st.error(f"Error connecting to API: {e}")

# Run the Streamlit app
if __name__ == "__main__":
    # This is handled by Streamlit CLI when running `streamlit run app.py`
    pass