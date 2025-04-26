# In legal_analysis.py, add the proper OpenAI import and configuration
import os
import json
import openai
from dotenv import load_dotenv
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

# Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY", "your-api-key-here")  # Replace with your actual key if needed


class LegalAnalyzer:
    def __init__(self):
        self.model = "gpt-4o"  # Use a powerful model for legal analysis

    def generate_summary(self, text: str) -> str:
        """Generate a plain language summary of a legal document"""
        if not text:
            return "No text provided for summarization."
        
        try:
            prompt = f"""
            Please provide a concise summary of the following legal text in plain language. 
            Focus on the key obligations, rights, and important clauses.
            
            Text: {text[:4000]}  # Limiting input size
            
            Summary:
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a legal expert specializing in contract analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating summary: {e}")
            return "Error generating summary. Please try again."
    
    def identify_risks(self, text: str) -> List[Dict[str, Any]]:
        """Identify potential risks in the legal document"""
        if not text:
            return []
        
        try:
            prompt = f"""
            Please analyze the following legal text and identify the top 5 potential risks or issues.
            For each risk, provide:
            1. A short description of the risk
            2. The severity (High, Medium, Low)
            3. The specific clause or text that indicates this risk
            
            Format your response as a JSON array with objects containing "description", "severity", and "clause".
            
            Text: {text[:4000]}  # Limiting input size
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a legal expert specializing in risk assessment."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.2
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON from the response
            try:
                # Find JSON array in the response
                start_idx = content.find('[')
                end_idx = content.rfind(']') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = content[start_idx:end_idx]
                    risks = json.loads(json_str)
                    return risks
                return []
            except:
                # Fallback if JSON parsing fails
                return [{"description": "Error parsing risk analysis results", "severity": "Unknown", "clause": ""}]
        except Exception as e:
            print(f"Error identifying risks: {e}")
            return []
    
    def compare_documents(self, doc1: str, doc2: str) -> Dict[str, Any]:
        """Compare two legal documents and identify differences"""
        if not doc1 or not doc2:
            return {"error": "Two documents are required for comparison"}
        
        try:
            prompt = f"""
            Please compare these two legal texts and identify key differences in terms of:
            1. Obligations and rights
            2. Important clauses like governing law, termination, etc.
            3. Risk allocation
            
            Format your response as a JSON object with these categories.
            
            Text 1: {doc1[:2000]}  # Limiting input size
            
            Text 2: {doc2[:2000]}  # Limiting input size
            """
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a legal expert specializing in contract comparison."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.2
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON from the response
            try:
                # Find JSON object in the response
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                if start_idx >= 0 and end_idx > start_idx:
                    json_str = content[start_idx:end_idx]
                    comparison = json.loads(json_str)
                    return comparison
                return {"error": "Could not parse comparison results"}
            except:
                # Fallback if JSON parsing fails
                return {"error": "Error parsing comparison results"}
        except Exception as e:
            print(f"Error comparing documents: {e}")
            return {"error": str(e)}