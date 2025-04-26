# backend/document_processor.py
import PyPDF2
import re
from typing import List, Dict, Any, Tuple
from io import BytesIO

class LegalDocumentProcessor:
    def __init__(self):
        # Common legal clause keywords to identify sections
        self.clause_keywords = {
            "governing_law": ["govern", "law", "jurisdiction"],
            "termination": ["terminat", "cancel", "end"],
            "indemnification": ["indemnif", "hold harmless", "defend"],
            "confidentiality": ["confidential", "proprietary", "non-disclosure"],
            "assignment": ["assign", "transfer", "delegation"],
            "payment_terms": ["payment", "fee", "compensation"],
            "limitation_liability": ["limit", "liability", "responsible"],
            "force_majeure": ["force majeure", "act of god", "unforeseen"],
            "non_compete": ["non-compete", "competition", "restraint of trade"],
            "warranties": ["warrant", "represent", "guarantee"]
        }
    
    def extract_text_from_pdf(self, pdf_file: bytes) -> str:
        """Extract text from a PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(BytesIO(pdf_file))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""

    def extract_text_from_txt(self, text_file: bytes) -> str:
        """Extract text from a TXT file"""
        try:
            return text_file.decode('utf-8')
        except Exception as e:
            print(f"Error extracting text from TXT: {e}")
            return ""
            
    def chunk_document(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """Split document into overlapping chunks"""
        chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i:i + chunk_size]
            chunks.append(chunk)
        return chunks
    
    def extract_legal_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract basic legal entities from text"""
        entities = {
            "parties": [],
            "dates": [],
            "monetary_values": [],
            "addresses": []
        }
        
        # Simple regex patterns for demonstration
        # In a production system, you'd use a more sophisticated NER approach
        party_pattern = re.compile(r'(?:(?:the )?([A-Z][a-z]+ [A-Z][a-z]+)|(?:the )?([A-Z][A-Z]+))')
        date_pattern = re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b')
        money_pattern = re.compile(r'\$\s*\d+(?:,\d{3})*(?:\.\d{2})?|\d+(?:,\d{3})*(?:\.\d{2})?\s*dollars')
        
        # Extract entities using regex
        party_matches = party_pattern.findall(text)
        entities["parties"] = [match[0] or match[1] for match in party_matches if any(match)]
        
        entities["dates"] = date_pattern.findall(text)
        entities["monetary_values"] = money_pattern.findall(text)
        
        return entities
    
    def identify_clause_types(self, text: str) -> Dict[str, List[Tuple[str, str]]]:
        """Identify different types of clauses in the text"""
        clauses = {}
        paragraphs = re.split(r'\n\s*\n', text)
        
        for clause_type, keywords in self.clause_keywords.items():
            clauses[clause_type] = []
            
            for paragraph in paragraphs:
                if any(keyword.lower() in paragraph.lower() for keyword in keywords):
                    # Get first 50 characters as a preview
                    preview = paragraph[:50] + "..." if len(paragraph) > 50 else paragraph
                    clauses[clause_type].append((preview, paragraph))
        
        return clauses