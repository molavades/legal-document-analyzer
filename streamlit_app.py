import streamlit as st
import sys
import os
import subprocess
import threading
import time

# Set up secrets access
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    os.environ["PINECONE_API_KEY"] = st.secrets["PINECONE_API_KEY"]
    os.environ["PINECONE_ENVIRONMENT"] = st.secrets["PINECONE_ENVIRONMENT"]

# Set page configuration
st.set_page_config(
    page_title="Legal Document Analyzer",
    page_icon="⚖️",
    layout="wide"
)

# Start FastAPI in a separate thread
def run_api():
    from fastapi import FastAPI
    import uvicorn
    import importlib.util
    
    # Import app dynamically
    spec = importlib.util.spec_from_file_location("app", "./backend/app.py")
    app_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(app_module)
    
    # Set environment variable for frontend to connect to local API
    os.environ["API_URL"] = "http://localhost:8000"
    
    # Run FastAPI
    uvicorn.run(app_module.app, host="0.0.0.0", port=8000)

# Start API in separate thread
thread = threading.Thread(target=run_api, daemon=True)
thread.start()

# Give API time to start
time.sleep(5)

# Import frontend
from frontend.app import *
