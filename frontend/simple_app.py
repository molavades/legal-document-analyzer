import streamlit as st

st.title("⚖️ Legal Document Analyzer")
st.markdown("A tool for legal professionals to analyze contracts and legal documents")

st.write("## Project Overview")
st.write("This application provides legal professionals with tools to:")
st.write("- Extract key clauses, entities, and obligations from legal documents")
st.write("- Compare documents side-by-side to identify differences")
st.write("- Generate plain-language summaries and risk assessments")

st.write("## Features")
st.write("- **Document Analysis**: Extract entities, clauses, and relationships")
st.write("- **Semantic Search**: Find relevant information across documents")
st.write("- **Risk Assessment**: Identify potential legal risks")
st.write("- **Document Comparison**: Compare clauses across different documents")

st.write("## Technology")
st.write("- **Vector Database**: For efficient semantic retrieval")
st.write("- **LLM Integration**: OpenAI GPT-4o for legal understanding")
st.write("- **FastAPI Backend**: For processing and analysis")

st.write("## Demo")
st.image("https://github.com/user-attachments/assets/31d801ad-6f63-4788-b667-f44a7bcc3c23", 
         caption="Document Analysis Page")
