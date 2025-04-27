import streamlit as st
import sys
import os

# Configure secrets first - before any other Streamlit commands
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    os.environ["PINECONE_API_KEY"] = st.secrets.get("PINECONE_API_KEY", "")
    os.environ["PINECONE_ENVIRONMENT"] = st.secrets.get("PINECONE_ENVIRONMENT", "gcp-starter")

# Set page configuration (must come before any other Streamlit commands)
st.set_page_config(
    page_title="Legal Document Analyzer",
    page_icon="⚖️",
    layout="wide"
)

# Display a simpler frontend-only version for Streamlit Cloud
st.title("⚖️ Legal Document Analysis System")

# Add tab menu
tab1, tab2 = st.tabs(["Documents", "About"])

with tab1:
    st.write("### Upload a Document")
    
    # File uploader
    uploaded_file = st.file_uploader("Choose a PDF or TXT file", type=["pdf", "txt"])
    
    if uploaded_file:
        # Basic file display
        st.write(f"**Filename:** {uploaded_file.name}")
        st.write(f"**File size:** {uploaded_file.size} bytes")
        
        # Basic text extraction (minimal functionality)
        if uploaded_file.type == "application/pdf":
            st.write("PDF content will be processed by our backend...")
        else:
            # Display text content
            text_content = uploaded_file.read().decode()
            st.text_area("Document Content", text_content, height=300)
        
        # Simulate analysis (for demo purposes)
        if st.button("Analyze Document"):
            with st.spinner("Analyzing document..."):
                st.success("Analysis complete! This is a simplified demo.")
                
                # Mock analysis results
                st.write("### Document Summary")
                st.write("This is a legal document containing various clauses and provisions.")
                
                st.write("### Key Entities")
                st.json({
                    "parties": ["Company A", "Company B"],
                    "dates": ["2023-01-15", "2024-12-31"],
                    "monetary_values": ["$50,000", "$1,000,000"]
                })
                
                st.write("### Risk Assessment")
                st.warning("Medium risk: Incomplete termination clause")
                st.info("Low risk: Standard confidentiality provisions")

with tab2:
    st.write("### About This Project")
    st.write("""
    This Legal Document Analysis System is designed to help legal professionals efficiently analyze contracts and legal documents.
    
    The full version of this application includes:
    - Automated extraction of key clauses and entities
    - Risk assessment of legal provisions
    - Plain language summaries of complex legal text
    - Document comparison capabilities
    - Semantic search across documents
    
    This project was developed as part of a portfolio project demonstrating the capabilities of AI in legal document analysis.
    """)
    
    st.write("### Technologies Used")
    st.write("""
    - Python 3.10
    - Streamlit
    - OpenAI API
    - Pinecone Vector Database
    - FastAPI (backend)
    """)
