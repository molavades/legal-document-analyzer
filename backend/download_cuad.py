# backend/download_cuad_direct.py
import os
import requests
import zipfile
import io
import shutil
from pathlib import Path

def download_cuad_direct():
    """Download CUAD dataset directly from Zenodo"""
    print("Downloading CUAD dataset from Zenodo...")
    
    # Create data directory if it doesn't exist
    data_dir = Path("../data")
    data_dir.mkdir(exist_ok=True)
    
    # Updated direct download URL from Zenodo
    download_url = "https://zenodo.org/api/files/08615d53-fa14-438d-b6f3-9533061a2532/CUAD_v1.zip"
    
    try:
        # Download the zip file
        print(f"Downloading from {download_url}...")
        response = requests.get(download_url, stream=True)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Save the zip file
        zip_path = data_dir / "CUAD_v1.zip"
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"Downloaded zip file to {zip_path}")
        
        # Extract the zip file
        print("Extracting files...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(data_dir / "cuad")
        
        # Optional: Remove the zip file after extraction
        os.remove(zip_path)
        
        print("CUAD dataset downloaded and extracted successfully!")
        
        # Print information about the extracted files
        cuad_dir = data_dir / "cuad"
        
        # Count files by type
        pdf_count = len(list(cuad_dir.glob("**/*.pdf")))
        txt_count = len(list(cuad_dir.glob("**/*.txt")))
        json_count = len(list(cuad_dir.glob("**/*.json")))
        excel_count = len(list(cuad_dir.glob("**/*.xlsx")))
        
        print(f"Dataset contents:")
        print(f"- PDF files: {pdf_count}")
        print(f"- TXT files: {txt_count}")
        print(f"- JSON files: {json_count}")
        print(f"- Excel files: {excel_count}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error downloading the dataset: {e}")
    except zipfile.BadZipFile:
        print("Error: The downloaded file is not a valid zip file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    download_cuad_direct()