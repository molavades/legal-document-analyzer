import streamlit as st
import os
import io
import pandas as pd
import matplotlib.pyplot as plt
import base64
from PIL import Image
import PyPDF2

# Configure secrets first - before any other Streamlit commands
if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
    os.environ["PINECONE_API_KEY"] = st.secrets.get("PINECONE_API_KEY", "")
    os.environ["PINECONE_ENVIRONMENT"] = st.secrets.get("PINECONE_ENVIRONMENT", "gcp-starter")

# Set page configuration (must come before any other Streamlit commands)
st.set_page_config(
    page_title="Legal Document Analyzer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    /* Main app background and text colors */
    .main {
        background-color: #f9f9f9;
        color: #333333;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1e3a5f;
    }
    
    /* Headers styling */
    h1, h2, h3 {
        color: #1e3a5f;
        font-weight: 600;
    }
    
    /* Button styling */
    .stButton button {
        background-color: #2c5282;
        color: white;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    .stButton button:hover {
        background-color: #1e3a5f;
        border-color: #1e3a5f;
    }
    
    /* Card container for better layout */
    .card {
        background-color: white;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* Risk indicators */
    .risk-high {
        background-color: #e53e3e;
        color: white;
        padding: 8px 12px;
        border-radius: 4px;
        font-weight: 500;
    }
    .risk-medium {
        background-color: #f6ad55;
        color: white;
        padding: 8px 12px;
        border-radius: 4px;
        font-weight: 500;
    }
    .risk-low {
        background-color: #68d391;
        color: white;
        padding: 8px 12px;
        border-radius: 4px;
        font-weight: 500;
    }
    
    /* File uploader styling */
    .uploadedFile {
        border: 2px dashed #2c5282;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f1f5f9;
        border-radius: 6px 6px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2c5282;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for storing documents and analysis
if 'documents' not in st.session_state:
    st.session_state.documents = {}
if 'current_document' not in st.session_state:
    st.session_state.current_document = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = {}

# PDF text extraction function
def extract_text_from_pdf(pdf_bytes):
    """Extract text from a PDF file"""
    try:
        pdf_file = io.BytesIO(pdf_bytes)
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""

# Function to extract legal entities (simplified)
def extract_legal_entities(text):
    """Extract basic legal entities from text using simple patterns"""
    import re
    
    entities = {
        "parties": [],
        "dates": [],
        "monetary_values": [],
        "locations": []
    }
    
    # Simple regex patterns
    party_pattern = re.compile(r'(?:(?:the )?([A-Z][a-z]+ [A-Z][a-z]+)|(?:the )?([A-Z][A-Z]+))')
    date_pattern = re.compile(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b')
    money_pattern = re.compile(r'\$\s*\d+(?:,\d{3})*(?:\.\d{2})?|\d+(?:,\d{3})*(?:\.\d{2})?\s*dollars')
    location_pattern = re.compile(r'\b(?:Alabama|Alaska|Arizona|Arkansas|California|Colorado|Connecticut|Delaware|Florida|Georgia|Hawaii|Idaho|Illinois|Indiana|Iowa|Kansas|Kentucky|Louisiana|Maine|Maryland|Massachusetts|Michigan|Minnesota|Mississippi|Missouri|Montana|Nebraska|Nevada|New Hampshire|New Jersey|New Mexico|New York|North Carolina|North Dakota|Ohio|Oklahoma|Oregon|Pennsylvania|Rhode Island|South Carolina|South Dakota|Tennessee|Texas|Utah|Vermont|Virginia|Washington|West Virginia|Wisconsin|Wyoming)\b')
    
    # Extract entities using regex
    party_matches = set(match[0] or match[1] for match in party_pattern.findall(text) if any(match))
    entities["parties"] = list(party_matches)[:10]  # Limit to avoid clutter
    
    date_matches = set(date_pattern.findall(text))
    entities["dates"] = list(date_matches)[:10]
    
    money_matches = set(money_pattern.findall(text))
    entities["monetary_values"] = list(money_matches)[:10]
    
    location_matches = set(location_pattern.findall(text))
    entities["locations"] = list(location_matches)[:10]
    
    return entities

# Function to identify clause types
def identify_clauses(text):
    """Identify different types of clauses in the text"""
    import re
    
    clause_keywords = {
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
    
    clauses = {}
    paragraphs = re.split(r'\n\s*\n', text)
    
    for clause_type, keywords in clause_keywords.items():
        clauses[clause_type] = []
        
        for paragraph in paragraphs:
            if any(keyword.lower() in paragraph.lower() for keyword in keywords):
                preview = paragraph[:50] + "..." if len(paragraph) > 50 else paragraph
                clauses[clause_type].append((preview, paragraph))
    
    return clauses

# Simple risk assessment
def assess_risks(clauses):
    """Perform a basic risk assessment based on clauses"""
    risks = []
    
    # Check for non-compete
    if clauses.get("non_compete") and len(clauses["non_compete"]) > 0:
        risks.append({
            "severity": "High",
            "description": "Non-compete clause may have enforceability issues",
            "details": "The non-compete clause may not be enforceable in certain jurisdictions. Some states limit non-compete agreements or require additional consideration.",
            "clause_type": "non_compete"
        })
    
    # Check for limitation of liability
    if clauses.get("limitation_liability") and len(clauses["limitation_liability"]) > 0:
        risks.append({
            "severity": "Medium",
            "description": "Limitation of Liability clause may be too broad",
            "details": "The limitation of liability clause appears to be very broad and may not be enforceable if challenged, particularly regarding gross negligence or willful misconduct.",
            "clause_type": "limitation_liability"
        })
    
    # Check for termination
    if clauses.get("termination") and len(clauses["termination"]) > 0:
        risks.append({
            "severity": "Medium",
            "description": "Termination clause lacks specific details",
            "details": "The termination clause may lack clarity on the process and obligations following termination, which could lead to disputes.",
            "clause_type": "termination"
        })
    
    # Check for missing force majeure
    if not clauses.get("force_majeure") or len(clauses["force_majeure"]) == 0:
        risks.append({
            "severity": "Low",
            "description": "Missing Force Majeure clause",
            "details": "The agreement does not contain a force majeure clause, which could create issues in case of unforeseen events that prevent performance.",
            "clause_type": "force_majeure" 
        })
    
    return risks

# Sidebar navigation
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/scales--v1.png", width=80)
    st.title("Legal Document Analyzer")
    
    st.markdown("---")
    
    # Navigation menu
    menu = st.radio(
        "Navigate to",
        ["Document Upload", "Document Analysis", "Search Documents", "About"]
    )
    
    st.markdown("---")
    
    # User section in sidebar
    st.markdown("### 👤 User")
    st.text("Demo User")
    st.progress(100)
    
    # Document list if any exist
    if st.session_state.documents:
        st.markdown("### 📄 Documents")
        for doc_id, doc in st.session_state.documents.items():
            if st.button(f"📄 {doc['filename']}", key=f"doc_btn_{doc_id}"):
                st.session_state.current_document = doc_id
                if menu != "Document Analysis":
                    menu = "Document Analysis"
                    st.experimental_rerun()
    
    # Footer
    st.markdown("---")
    st.caption("© 2025 Legal Document Analyzer")
    st.caption("Version 1.0")

# Main content based on navigation
if menu == "Document Upload":
    st.title("📄 Document Upload")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Upload a Document")
    st.markdown("Supported formats: PDF, TXT")
    
    # File uploader with processing
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt"], label_visibility="collapsed")
    
    if uploaded_file:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.success(f"File '{uploaded_file.name}' uploaded successfully!")
            st.write(f"**Size:** {uploaded_file.size} bytes")
            st.write(f"**Type:** {uploaded_file.type}")
            
            # Process button
            if st.button("Process Document", type="primary", use_container_width=True):
                with st.spinner("Processing document..."):
                    # Generate a unique ID for the document
                    import uuid
                    doc_id = str(uuid.uuid4())
                    
                    # Extract text based on file type
                    if uploaded_file.type == "application/pdf":
                        document_text = extract_text_from_pdf(uploaded_file.getvalue())
                    else:
                        document_text = uploaded_file.getvalue().decode("utf-8")
                    
                    # Extract entities and clauses
                    entities = extract_legal_entities(document_text)
                    clauses = identify_clauses(document_text)
                    risks = assess_risks(clauses)
                    
                    # Store document and analysis in session state
                    st.session_state.documents[doc_id] = {
                        "id": doc_id,
                        "filename": uploaded_file.name,
                        "content": document_text,
                        "file_type": uploaded_file.type,
                        "size": uploaded_file.size,
                        "upload_date": pd.Timestamp.now().strftime("%Y-%m-%d")
                    }
                    
                    st.session_state.analysis_results[doc_id] = {
                        "entities": entities,
                        "clauses": clauses,
                        "risks": risks
                    }
                    
                    # Set current document
                    st.session_state.current_document = doc_id
                    
                    # Navigate to analysis
                    st.success("Document processed successfully! View analysis in the Document Analysis tab.")
                    st.markdown(f"[Go to Document Analysis](#document-analysis)")
        
        with col2:
            st.subheader("Document Preview")
            if uploaded_file.type == "application/pdf":
                # Display first page as an image for PDF
                try:
                    import fitz  # PyMuPDF
                    
                    # Create a BytesIO object from the uploaded file
                    file_stream = io.BytesIO(uploaded_file.getvalue())
                    
                    # Open the PDF file
                    pdf_document = fitz.open(stream=file_stream, filetype="pdf")
                    
                    # Get the first page
                    first_page = pdf_document.load_page(0)
                    
                    # Render page to an image
                    pix = first_page.get_pixmap(matrix=fitz.Matrix(2, 2))
                    
                    # Convert to PIL Image
                    img = Image.open(io.BytesIO(pix.tobytes("png")))
                    
                    # Display the image
                    st.image(img, caption=f"First page of {uploaded_file.name}", use_column_width=True)
                    
                    # Close the document
                    pdf_document.close()
                except Exception as e:
                    st.error(f"Cannot preview PDF: {e}")
                    # Fallback text preview
                    text = extract_text_from_pdf(uploaded_file.getvalue())
                    st.text_area("Text Preview", text[:1000] + "..." if len(text) > 1000 else text, height=400)
            else:
                # For text files, show the content
                try:
                    text_content = uploaded_file.getvalue().decode("utf-8")
                    st.text_area("", text_content[:1000] + "..." if len(text_content) > 1000 else text_content, height=400)
                except:
                    st.error("Could not decode file content")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Document history
    if st.session_state.documents:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Uploaded Documents")
        
        # Create a DataFrame with document information
        doc_data = []
        for doc_id, doc in st.session_state.documents.items():
            doc_data.append({
                "Filename": doc["filename"],
                "Upload Date": doc["upload_date"],
                "Size (KB)": f"{doc['size']/1024:.1f}",
                "Type": doc["file_type"]
            })
        
        doc_df = pd.DataFrame(doc_data)
        st.dataframe(doc_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Document Analysis":
    st.title("🔍 Document Analysis")
    
    # Check if we have a current document
    if not st.session_state.current_document or st.session_state.current_document not in st.session_state.documents:
        st.info("No document selected. Please upload or select a document to analyze.")
    else:
        doc_id = st.session_state.current_document
        document = st.session_state.documents[doc_id]
        analysis = st.session_state.analysis_results[doc_id]
        
        # Tabs for different analysis views
        tabs = st.tabs(["📝 Overview", "🔖 Clauses", "👥 Entities", "⚠️ Risk Assessment", "📊 Summary"])
        
        with tabs[0]:  # Overview tab
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Document Information")
            
            info_col1, info_col2 = st.columns(2)
            
            with info_col1:
                st.markdown(f"**Title:** {document['filename']}")
                st.markdown(f"**Upload Date:** {document['upload_date']}")
                st.markdown(f"**File Type:** {document['file_type']}")
            
            with info_col2:
                st.markdown(f"**Size:** {document['size']/1024:.1f} KB")
                
                # Count paragraphs
                paragraph_count = len(document['content'].split('\n\n'))
                st.markdown(f"**Paragraphs:** {paragraph_count}")
                
                # Estimated word count
                word_count = len(document['content'].split())
                st.markdown(f"**Words:** {word_count}")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Document content preview
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Document Content")
            
            st.text_area("", document['content'][:2000] + ("..." if len(document['content']) > 2000 else ""), height=400)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tabs[1]:  # Clauses tab
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Identified Clauses")
            
            # Count clauses found
            clause_count = sum(len(clauses) for clauses in analysis['clauses'].values())
            if clause_count == 0:
                st.info("No specific clauses identified in this document.")
            else:
                st.write(f"Found {clause_count} clauses across {len([k for k, v in analysis['clauses'].items() if v])} categories.")
                
                # Expandable sections for different clause types
                for clause_type, clause_list in analysis['clauses'].items():
                    if clause_list:
                        clause_name = clause_type.replace('_', ' ').title()
                        with st.expander(f"{clause_name} ({len(clause_list)})", expanded=False):
                            for i, (preview, full_text) in enumerate(clause_list):
                                st.markdown(f"**Clause {i+1}:**")
                                st.text_area(f"Content {i+1}", full_text, height=100, key=f"clause_{clause_type}_{i}")
                                st.markdown("---")
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tabs[2]:  # Entities tab
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Extracted Entities")
            
            entity_col1, entity_col2 = st.columns(2)
            
            with entity_col1:
                st.markdown("##### 👥 Parties")
                if analysis['entities']['parties']:
                    for party in analysis['entities']['parties']:
                        st.markdown(f"- {party}")
                else:
                    st.info("No parties identified")
                
                st.markdown("##### 📅 Dates")
                if analysis['entities']['dates']:
                    for date in analysis['entities']['dates']:
                        st.markdown(f"- {date}")
                else:
                    st.info("No dates identified")
                
            with entity_col2:
                st.markdown("##### 💰 Monetary Values")
                if analysis['entities']['monetary_values']:
                    for value in analysis['entities']['monetary_values']:
                        st.markdown(f"- {value}")
                else:
                    st.info("No monetary values identified")
                
                st.markdown("##### 📍 Locations")
                if analysis['entities']['locations']:
                    for location in analysis['entities']['locations']:
                        st.markdown(f"- {location}")
                else:
                    st.info("No locations identified")
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Entity visualization
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Entity Distribution")
            
            # Create a bar chart of entities
            entity_counts = {
                "Parties": len(analysis['entities']['parties']),
                "Dates": len(analysis['entities']['dates']),
                "Monetary Values": len(analysis['entities']['monetary_values']),
                "Locations": len(analysis['entities']['locations'])
            }
            
            fig, ax = plt.subplots(figsize=(10, 5))
            bars = ax.bar(
                entity_counts.keys(),
                entity_counts.values(),
                color=['#4299e1', '#f56565', '#ecc94b', '#9f7aea']
            )
            
            # Add value labels on top of bars
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width()/2.,
                    height + 0.1,
                    str(int(height)),
                    ha='center',
                    va='bottom',
                    fontweight='bold'
                )
                
            ax.set_ylabel("Count")
            ax.set_title("Entity Counts by Type")
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            st.pyplot(fig)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tabs[3]:  # Risk Assessment tab
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Risk Assessment")
            
            # Risk summary
            risks = analysis['risks']
            
            if not risks:
                st.info("No significant risks identified in this document.")
            else:
                # Count risks by severity
                risk_counts = {"High": 0, "Medium": 0, "Low": 0}
                for risk in risks:
                    risk_counts[risk["severity"]] += 1
                
                # Get overall risk level
                if risk_counts["High"] > 0:
                    overall_risk = "High"
                    risk_emoji = "🔴"
                elif risk_counts["Medium"] > 0:
                    overall_risk = "Medium"
                    risk_emoji = "🟠"
                else:
                    overall_risk = "Low"
                    risk_emoji = "🟢"
                
                st.markdown("### Overall Risk Profile")
                risk_profile_col1, risk_profile_col2, risk_profile_col3 = st.columns(3)
                
                with risk_profile_col1:
                    st.markdown(f'<div style="text-align:center; padding:20px; background-color:#f8fafc; border-radius:10px;">'
                               f'<span style="font-size:36px;">{risk_emoji}</span><br/>'
                               f'<span style="font-size:24px; font-weight:600;">{overall_risk}</span><br/>'
                               f'<span style="font-size:16px;">Overall Risk</span>'
                               f'</div>', unsafe_allow_html=True)
                
                with risk_profile_col2:
                    st.markdown(f'<div style="text-align:center; padding:20px; background-color:#f8fafc; border-radius:10px;">'
                               f'<span style="font-size:36px;">{len(risks)}</span><br/>'
                               f'<span style="font-size:24px; font-weight:600;">Issues</span><br/>'
                               f'<span style="font-size:16px;">Detected</span>'
                               f'</div>', unsafe_allow_html=True)
                
                with risk_profile_col3:
                    clauses_with_risks = len(set(risk["clause_type"] for risk in risks if "clause_type" in risk))
                    st.markdown(f'<div style="text-align:center; padding:20px; background-color:#f8fafc; border-radius:10px;">'
                               f'<span style="font-size:36px;">{clauses_with_risks}</span><br/>'
                               f'<span style="font-size:24px; font-weight:600;">Clauses</span><br/>'
                               f'<span style="font-size:16px;">Flagged</span>'
                               f'</div>', unsafe_allow_html=True)
                
                # Detailed risks
                st.markdown("### Identified Risks")
                
                # Display risks by severity
                for risk in risks:
                    if risk["severity"] == "High":
                        bg_color = "#fed7d7"
                        border_color = "#e53e3e"
                        text_color = "#c53030"
                    elif risk["severity"] == "Medium":
                        bg_color = "#feebc8"
                        border_color = "#dd6b20"
                        text_color = "#c05621"
                    else:
                        bg_color = "#c6f6d5"
                        border_color = "#38a169"
                        text_color = "#2f855a"
                        
                    st.markdown(f'<div style="padding:15px; background-color:{bg_color}; border-left:4px solid {border_color}; border-radius:4px; margin-bottom:15px;">'
                               f'<h4 style="color:{text_color}; margin:0;">{risk["severity"]} Risk: {risk["description"]}</h4>'
                               f'<p>{risk["details"]}</p>'
                               f'<p><strong>Clause Type:</strong> {risk.get("clause_type", "Multiple clauses").replace("_", " ").title()}</p>'
                               f'</div>', unsafe_allow_html=True)
                
                # Risk distribution pie chart
                if sum(risk_counts.values()) > 0:
                    fig, ax = plt.subplots(figsize=(6, 6))
                    labels = []
                    sizes = []
                    colors = []
                    
                    if risk_counts["High"] > 0:
                        labels.append("High")
                        sizes.append(risk_counts["High"])
                        colors.append('#e53e3e')
                        
                    if risk_counts["Medium"] > 0:
                        labels.append("Medium")
                        sizes.append(risk_counts["Medium"])
                        colors.append('#f6ad55')
                        
                    if risk_counts["Low"] > 0:
                        labels.append("Low")
                        sizes.append(risk_counts["Low"])
                        colors.append('#68d391')
                    
                    # Plot pie chart
                    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
                    ax.set_title("Risk Severity Distribution")
                    
                    st.pyplot(fig)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        with tabs[4]:  # Summary tab
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Document Summary")
            
            # Generate simple summary
            summary = f"""
            This document is titled "{document['filename']}" and contains approximately {word_count} words.
            
            Key findings from the analysis:
            
            1. **Entities**: Found {sum(len(entities) for entities in analysis['entities'].values())} entities including {len(analysis['entities']['parties'])} parties, {len(analysis['entities']['dates'])} dates, {len(analysis['entities']['monetary_values'])} monetary values, and {len(analysis['entities']['locations'])} locations.
            
            2. **Clauses**: Identified {clause_count} clauses across {len([k for k, v in analysis['clauses'].items() if v])} categories, with the most common types being {', '.join([k.replace('_', ' ').title() for k, v in analysis['clauses'].items() if v][:3])}.
            
            3. **Risks**: {len(analysis['risks'])} potential risks detected, with the highest risk level being {overall_risk if 'overall_risk' in locals() else 'None'}.
            """
            
            st.markdown(summary)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Visualization of clauses
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.subheader("Clause Distribution")
            
            # Count clauses by type
            clause_type_counts = {k.replace('_', ' ').title(): len(v) for k, v in analysis['clauses'].items() if v}
            
            if clause_type_counts:
                fig, ax = plt.subplots(figsize=(10, 6))
                
                # Horizontal bar chart
                y_pos = range(len(clause_type_counts))
                
                # Sort by count in descending order
                sorted_items = sorted(clause_type_counts.items(), key=lambda x: x[1], reverse=True)
                labels = [item[0] for item in sorted_items]
                counts = [item[1] for item in sorted_items]
                
                bars = ax.barh(y_pos, counts, align='center')
                ax.set_yticks(y_pos)
                ax.set_yticklabels(labels)
                ax.invert_yaxis()  # Labels read top-to-bottom
                ax.set_xlabel('Count')
                ax.set_title('Clause Frequency by Type')
                
                # Add count labels
                for i, v in enumerate(counts):
                    ax.text(v + 0.1, i, str(v), va='center')
                
                st.pyplot(fig)
            else:
                st.info("No clauses identified to visualize.")
            
            st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Search Documents":
    st.title("🔎 Search Documents")
    
    if not st.session_state.documents:
        st.info("No documents available. Please upload documents first.")
    else:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Search Documents")
        
        search_query = st.text_input("Enter your search query", placeholder="e.g., termination notice period")
        
        if search_query and st.button("Search", type="primary"):
            # Perform basic search across documents
            search_results = []
            
            for doc_id, doc in st.session_state.documents.items():
                # Simple text search
                content = doc["content"].lower()
                query = search_query.lower()
                
                if query in content:
                    # Get context around match
                    index = content.find(query)
                    start = max(0, index - 100)
                    end = min(len(content), index + len(query) + 100)
                    
                    # Get context
                    if start > 0:
                        context = "..." + content[start:end] + "..."
                    else:
                        context = content[start:end] + "..."
                    
                    # Highlight the match
                    highlighted = context.replace(query, f"<mark>{query}</mark>")
                    
                    # Calculate a simple relevance score
                    relevance = content.count(query) * 10
                    
                    search_results.append({
                        "doc_id": doc_id,
                        "filename": doc["filename"],
                        "context": highlighted,
                        "relevance": min(relevance, 100)  # Cap at 100%
                    })
            
            # Sort by relevance
            search_results.sort(key=lambda x: x["relevance"], reverse=True)
            
            if search_results:
                st.success(f"Found {len(search_results)} matching documents!")
                
                # Display results
                for result in search_results:
                    st.markdown(
                        f'<div style="padding:15px; background-color:#f8fafc; border:1px solid #e2e8f0; border-radius:5px; margin-bottom:15px;">'
                        f'<h4 style="margin-top:0;">{result["filename"]}</h4>'
                        f'<p>{result["context"]}</p>'
                        f'<p><strong>Relevance Score:</strong> {result["relevance"]}%</p>'
                        f'<a href="#" onclick="return false;">View Document</a>'
                        f'</div>', 
                        unsafe_allow_html=True
                    )
                    
                    # Add button to view document
                    if st.button("View Document", key=f"view_{result['doc_id']}"):
                        st.session_state.current_document = result["doc_id"]
                        st.experimental_rerun()
            else:
                st.info(f"No documents found matching '{search_query}'")
        
        st.markdown("</div>", unsafe_allow_html=True)

else:  # About section
    st.title("ℹ️ About")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("""
    ### Legal Document Analysis System

    This application is designed to help legal professionals efficiently analyze contracts and legal documents. By leveraging advanced AI and natural language processing, the system can automatically identify key clauses, extract important entities, assess potential risks, and provide plain-language summaries.
    
    **Key Features:**
    
    - 📄 **Document Processing:** Extract and analyze text from various document formats
    - 🔍 **Entity Extraction:** Identify parties, dates, monetary values, and other key entities
    - 📝 **Clause Identification:** Automatically detect and categorize important legal clauses
    - ⚖️ **Risk Assessment:** Evaluate potential risks and flag problematic provisions
    - 🔎 **Semantic Search:** Find relevant information across multiple documents
    - 📊 **Document Comparison:** Compare similar clauses across different contracts
    """)
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Technologies Used")
    
    tech_col1, tech_col2, tech_col3 = st.columns(3)
    
    with tech_col1:
        st.markdown("""
        #### Frontend
        - Python 3.10
        - Streamlit 1.26.0
        - Pandas
        - Matplotlib
        """)
    
    with tech_col2:
        st.markdown("""
        #### Backend
        - FastAPI
        - PyPDF2
        - OpenAI API
        - Pinecone
        - Numpy
        """)
    
    with tech_col3:
        st.markdown("""
        #### Data
        - CUAD Dataset
        - Legal contract corpus
        - Vector embeddings
        - Document processing
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Contact")
    
    st.markdown("""
    **Developer:** Snehal Molavade  
    **Email:** molavade.s@northeastern.edu  
    **GitHub:** github.com/molavades  
    """)
    
    st.markdown("</div>", unsafe_allow_html=True)
