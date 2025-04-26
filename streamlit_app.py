import streamlit as st
import sys
import os
import subprocess
import threading
import time

# Set up environment variables from Streamlit secrets
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

# Start the FastAPI backend in a separate thread
def run_api():
    subprocess.Popen(["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"])

# Start the API thread
threading.Thread(target=run_api, daemon=True).start()
time.sleep(3)  # Give API time to start

# Set API URL for local environment
os.environ["API_URL"] = "http://localhost:8000"

# Import the frontend code
sys.path.insert(0, "./frontend")
from app import *  # This will run your frontend Streamlit code