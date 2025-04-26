import streamlit as st

st.set_page_config(page_title="Legal Document Analyzer", page_icon="⚖️", layout="wide")

# Header
st.title("⚖️ Legal Document Analysis System")
st.markdown("A tool for legal professionals to analyze contracts and legal documents")

# Project Overview
st.write("""
## Project Overview

This system helps legal professionals analyze contracts and legal documents by:
- Extracting key clauses, entities, and obligations
- Comparing documents to identify differences
- Generating plain language summaries and risk assessments
- Providing semantic search across document collections
""")

# Features with mock images
st.write("## Key Features")

col1, col2 = st.columns(2)

with col1:
    st.write("### Document Analysis")
    st.write("Upload and process legal documents to extract important information")
    
    st.write("### Entity Extraction")
    st.write("Automatically identify parties, dates, monetary values, and obligations")

with col2:
    st.write("### Risk Assessment")
    st.write("AI-powered identification of potential legal issues")
    
    st.write("### Document Comparison")
    st.write("Compare clauses between different documents to spot differences")

# Mock contract text
st.write("## Example Contract Analysis")

with st.expander("Sample Contract Clause: Governing Law"):
    st.write("""
    This Agreement shall be governed by and construed in accordance with the laws of the State of Delaware, 
    without giving effect to any choice of law or conflict of law provisions. The parties consent to the exclusive 
    jurisdiction and venue in the federal and state courts located in Delaware County, Delaware.
    """)
    
    st.write("**Extracted Information:**")
    st.write("- **Governing Jurisdiction:** Delaware")
    st.write("- **Venue:** Federal and state courts in Delaware County")
    st.write("- **Clause Type:** Governing Law")

# GitHub Repository Link
st.markdown("""
## Project Details

This demo is a simplified version of the full Legal Document Analysis System.

The complete code with functional backend is available in the [GitHub repository](https://github.com/molavades/legal-document-analyzer).

**Technologies used:**
- FastAPI backend
- LLM integration for legal analysis
- Vector search for document retrieval
- Streamlit frontend
""")

# Add footer
st.markdown("---")
st.markdown("© 2025 Legal Document Analysis System | Created for INFO 7390")
