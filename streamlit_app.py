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

# Sidebar navigation
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/scales--v1.png", width=80)
    st.title("Legal Document Analyzer")
    
    st.markdown("---")
    
    # Navigation menu
    menu = st.radio(
        "Navigate to",
        ["Dashboard", "Document Upload", "Document Analysis", "Search Documents", "About"]
    )
    
    st.markdown("---")
    
    # User section in sidebar
    st.markdown("### 👤 User")
    st.text("Demo User")
    st.progress(100)
    
    # Stats section
    st.markdown("### 📊 Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Documents", "5")
    with col2:
        st.metric("Analyzed", "3")
    
    # Footer
    st.markdown("---")
    st.caption("© 2025 Legal Document Analyzer")
    st.caption("Version 1.0")

# Main content based on navigation
if menu == "Dashboard":
    st.title("📊 Dashboard")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Recent Activity")
    
    # Recent activity metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Documents Uploaded", "5", "+2")
    with col2:
        st.metric("Risk Assessments", "3", "+1")
    with col3:
        st.metric("Clauses Extracted", "145", "+37")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Documents overview
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Your Documents")
    
    # Sample table
    data = {
        "Document": ["Employment Contract", "NDA Agreement", "Service Agreement", "License Agreement", "Lease Contract"],
        "Date": ["2025-04-20", "2025-04-18", "2025-04-15", "2025-04-10", "2025-04-05"],
        "Type": ["Employment", "Confidentiality", "Service", "License", "Lease"],
        "Status": ["Analyzed", "Analyzed", "Analyzed", "Pending", "Pending"]
    }
    
    # Convert to dataframe and display
    import pandas as pd
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Risk summary
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Risk Summary")
    
    risk_col1, risk_col2 = st.columns([3, 2])
    
    with risk_col1:
        import matplotlib.pyplot as plt
        import numpy as np
        
        # Sample data for risks
        labels = ['High', 'Medium', 'Low']
        sizes = [2, 5, 12]
        colors = ['#e53e3e', '#f6ad55', '#68d391']
        
        # Create a figure and plot
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        st.pyplot(fig)
        
    with risk_col2:
        st.markdown("#### Risk Distribution")
        st.markdown('<span class="risk-high">High Risk: 2</span>', unsafe_allow_html=True)
        st.write("")
        st.markdown('<span class="risk-medium">Medium Risk: 5</span>', unsafe_allow_html=True)
        st.write("")
        st.markdown('<span class="risk-low">Low Risk: 12</span>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Document Upload":
    st.title("📄 Document Upload")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Upload a Document")
    st.markdown("Supported formats: PDF, TXT")
    
    # Improved file uploader with styling
    upload_column, preview_column = st.columns([1, 1])
    
    with upload_column:
        uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt"], label_visibility="collapsed")
        
        if uploaded_file:
            st.success(f"File '{uploaded_file.name}' uploaded successfully!")
            st.write(f"**Size:** {uploaded_file.size} bytes")
            st.write(f"**Type:** {uploaded_file.type}")
            
            analyze_btn = st.button("Analyze Document", type="primary", use_container_width=True)
            if analyze_btn:
                st.session_state.current_page = "analysis"
    
    with preview_column:
        if uploaded_file:
            st.subheader("Document Preview")
            if uploaded_file.type == "application/pdf":
                st.info("PDF preview is not available in this demo version")
            else:
                try:
                    text_content = uploaded_file.read().decode()
                    st.text_area("", text_content[:500] + "...", height=200)
                except:
                    st.error("Could not decode file content")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Upload history
    if uploaded_file:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Recent Uploads")
        
        # Sample history
        history_data = {
            "Filename": [uploaded_file.name, "Previous_Document.pdf", "Old_Contract.pdf"],
            "Upload Date": ["2025-04-26", "2025-04-25", "2025-04-24"],
            "Size (KB)": [f"{uploaded_file.size/1024:.1f}", "245.3", "542.8"]
        }
        
        history_df = pd.DataFrame(history_data)
        st.dataframe(history_df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Document Analysis":
    st.title("🔍 Document Analysis")
    
    # Tabs for different analysis views
    tabs = st.tabs(["📝 Overview", "🔖 Clauses", "👥 Entities", "⚠️ Risk Assessment", "📊 Summary"])
    
    with tabs[0]:  # Overview tab
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Document Information")
        
        info_col1, info_col2 = st.columns(2)
        
        with info_col1:
            st.markdown("**Title:** Employment Agreement")
            st.markdown("**Type:** Employment Contract")
            st.markdown("**Date:** April 26, 2025")
            st.markdown("**Pages:** 12")
        
        with info_col2:
            st.markdown("**Format:** PDF")
            st.markdown("**Size:** 245 KB")
            st.markdown("**Status:** Analyzed")
            st.markdown("**Language:** English")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Document content preview
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Document Content")
        
        st.text_area("", """THIS EMPLOYMENT AGREEMENT (the "Agreement") is made and entered into as of April 26, 2025 (the "Effective Date"), by and between COMPANY INC., a Delaware corporation (the "Company"), and JOHN DOE, an individual (the "Employee").

WHEREAS, the Company desires to employ the Employee on the terms and conditions set forth herein; and

WHEREAS, the Employee desires to be employed by the Company on such terms and conditions.

NOW, THEREFORE, in consideration of the mutual covenants, promises, and obligations set forth herein, the parties agree as follows:

1. EMPLOYMENT TERM. The Employee's employment hereunder shall be effective as of the Effective Date and shall continue until terminated according to Section 5 of this Agreement. The period during which the Employee is employed by the Company hereunder is hereinafter referred to as the "Employment Term."
""", height=250)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[1]:  # Clauses tab
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Identified Clauses")
        
        # Expandable sections for different clause types
        with st.expander("Employment Term", expanded=True):
            st.markdown("""
            **Location:** Section 1\n
            **Content:** The Employee's employment hereunder shall be effective as of the Effective Date and shall continue until terminated according to Section 5 of this Agreement. The period during which the Employee is employed by the Company hereunder is hereinafter referred to as the "Employment Term."
            """)
            
        with st.expander("Compensation"):
            st.markdown("""
            **Location:** Section 3\n
            **Content:** For the services to be performed by the Employee during the Employment Term, the Company shall pay the Employee an annual base salary of $120,000, payable in accordance with the Company's customary payroll practices.
            """)
            
        with st.expander("Termination"):
            st.markdown("""
            **Location:** Section 5\n
            **Content:** This Agreement may be terminated by either party with thirty (30) days written notice. The Company may terminate the Employee's employment immediately for Cause, defined as: (i) the Employee's material breach of this Agreement; (ii) the Employee's conviction of, or plea of guilty or nolo contendere to, a felony; or (iii) the Employee's failure to follow lawful instructions.
            """)
            
        with st.expander("Non-Compete"):
            st.markdown("""
            **Location:** Section 8\n
            **Content:** For a period of twelve (12) months following the termination of the Employee's employment for any reason, the Employee shall not, directly or indirectly, engage in or prepare to engage in, or be employed by, any business that is engaging in or preparing to engage in any activity or line of business that competes with any activity or line of business that the Company conducts, offers or is preparing to conduct or offer.
            """)
            
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[2]:  # Entities tab
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Extracted Entities")
        
        entity_col1, entity_col2 = st.columns(2)
        
        with entity_col1:
            st.markdown("##### 👥 Parties")
            st.markdown("- COMPANY INC. (Company)")
            st.markdown("- JOHN DOE (Employee)")
            
            st.markdown("##### 📅 Dates")
            st.markdown("- April 26, 2025 (Effective Date)")
            st.markdown("- Thirty (30) days (Notice Period)")
            st.markdown("- Twelve (12) months (Non-compete Period)")
            
        with entity_col2:
            st.markdown("##### 💰 Monetary Values")
            st.markdown("- $120,000 (Annual Base Salary)")
            
            st.markdown("##### 📍 Locations")
            st.markdown("- Delaware (Incorporation State)")
            
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Entity relationships visualization
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Entity Relationships")
        
        # Simple network graph visualization
        import networkx as nx
        
        # Create a graph
        G = nx.Graph()
        
        # Add nodes
        G.add_node("COMPANY INC.", type="organization")
        G.add_node("JOHN DOE", type="person")
        G.add_node("Employment Agreement", type="document")
        G.add_node("$120,000", type="money")
        G.add_node("April 26, 2025", type="date")
        
        # Add edges
        G.add_edge("COMPANY INC.", "Employment Agreement", relation="party to")
        G.add_edge("JOHN DOE", "Employment Agreement", relation="party to")
        G.add_edge("COMPANY INC.", "JOHN DOE", relation="employs")
        G.add_edge("$120,000", "JOHN DOE", relation="salary of")
        G.add_edge("April 26, 2025", "Employment Agreement", relation="effective date of")
        
        # Plot
        fig, ax = plt.subplots(figsize=(8, 6))
        pos = nx.spring_layout(G, seed=42)
        
        # Draw nodes with different colors based on type
        nx.draw_networkx_nodes(G, pos, nodelist=[n for n, d in G.nodes(data=True) if d.get('type') == 'organization'], 
                             node_color='#4299e1', node_size=800, alpha=0.9)
        nx.draw_networkx_nodes(G, pos, nodelist=[n for n, d in G.nodes(data=True) if d.get('type') == 'person'], 
                             node_color='#f56565', node_size=800, alpha=0.9)
        nx.draw_networkx_nodes(G, pos, nodelist=[n for n, d in G.nodes(data=True) if d.get('type') == 'document'], 
                             node_color='#68d391', node_size=800, alpha=0.9)
        nx.draw_networkx_nodes(G, pos, nodelist=[n for n, d in G.nodes(data=True) if d.get('type') == 'money'], 
                             node_color='#ecc94b', node_size=800, alpha=0.9)
        nx.draw_networkx_nodes(G, pos, nodelist=[n for n, d in G.nodes(data=True) if d.get('type') == 'date'], 
                             node_color='#9f7aea', node_size=800, alpha=0.9)
        
        # Draw edges and labels
        nx.draw_networkx_edges(G, pos, width=2, alpha=0.7)
        nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif", font_weight="bold")
        
        ax.axis('off')
        st.pyplot(fig)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[3]:  # Risk Assessment tab
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Risk Assessment")
        
        # Risk summary
        st.markdown("### Overall Risk Profile")
        risk_profile_col1, risk_profile_col2, risk_profile_col3 = st.columns(3)
        
        with risk_profile_col1:
            st.markdown('<div style="text-align:center; padding:20px; background-color:#f8fafc; border-radius:10px;">'
                       '<span style="font-size:36px;">⚠️</span><br/>'
                       '<span style="font-size:24px; font-weight:600;">Medium</span><br/>'
                       '<span style="font-size:16px;">Overall Risk</span>'
                       '</div>', unsafe_allow_html=True)
        
        with risk_profile_col2:
            st.markdown('<div style="text-align:center; padding:20px; background-color:#f8fafc; border-radius:10px;">'
                       '<span style="font-size:36px;">3</span><br/>'
                       '<span style="font-size:24px; font-weight:600;">Issues</span><br/>'
                       '<span style="font-size:16px;">Detected</span>'
                       '</div>', unsafe_allow_html=True)
        
        with risk_profile_col3:
            st.markdown('<div style="text-align:center; padding:20px; background-color:#f8fafc; border-radius:10px;">'
                       '<span style="font-size:36px;">2</span><br/>'
                       '<span style="font-size:24px; font-weight:600;">Clauses</span><br/>'
                       '<span style="font-size:16px;">Flagged</span>'
                       '</div>', unsafe_allow_html=True)
        
        # Detailed risks
        st.markdown("### Identified Risks")
        
        st.markdown('<div style="padding:15px; background-color:#fed7d7; border-left:4px solid #e53e3e; border-radius:4px; margin-bottom:15px;">'
                   '<h4 style="color:#c53030; margin:0;">High Risk: Non-compete Duration</h4>'
                   '<p>The 12-month non-compete period may not be enforceable in certain jurisdictions. '
                   'Some states limit non-compete agreements or require additional consideration.</p>'
                   '<p><strong>Location:</strong> Section 8</p>'
                   '</div>', unsafe_allow_html=True)
        
        st.markdown('<div style="padding:15px; background-color:#feebc8; border-left:4px solid #dd6b20; border-radius:4px; margin-bottom:15px;">'
                   '<h4 style="color:#c05621; margin:0;">Medium Risk: Termination Clause</h4>'
                   '<p>The "for Cause" termination definition includes subjective elements that may be challenged. '
                   'The "failure to follow lawful instructions" provision is particularly broad.</p>'
                   '<p><strong>Location:</strong> Section 5</p>'
                   '</div>', unsafe_allow_html=True)
        
        st.markdown('<div style="padding:15px; background-color:#feebc8; border-left:4px solid #dd6b20; border-radius:4px; margin-bottom:15px;">'
                   '<h4 style="color:#c05621; margin:0;">Medium Risk: Missing Provisions</h4>'
                   '<p>The agreement lacks details on benefits, paid time off, and intellectual property rights. '
                   'These omissions could lead to disputes.</p>'
                   '<p><strong>Location:</strong> Various sections</p>'
                   '</div>', unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with tabs[4]:  # Summary tab
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Document Summary")
        
        st.markdown("""
        This Employment Agreement dated April 26, 2025, is between COMPANY INC. and JOHN DOE. Key terms include:

        1. **Employment Term**: Begins on the Effective Date and continues until terminated per Section 5.
        
        2. **Compensation**: Annual base salary of $120,000.
        
        3. **Termination**: Either party may terminate with 30 days' notice; the Company may terminate immediately for Cause.
        
        4. **Non-Compete**: 12-month restriction following termination.
        
        The agreement presents medium overall risk with three specific issues identified: (1) potentially unenforceable non-compete provisions, (2) subjective termination criteria, and (3) missing standard provisions regarding benefits and intellectual property.
        
        Recommended actions include reviewing the non-compete clause for enforceability in relevant jurisdictions and adding more specific language to the termination provisions.
        """)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Word cloud visualization
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.subheader("Key Terms Frequency")
        
        from wordcloud import WordCloud
        
        # Sample text for word cloud
        text = "employment agreement company employee term effective date termination cause section agreement compensation salary services notice period non-compete restrictive covenant confidential information intellectual property governing law jurisdiction amendment waiver severability entire agreement counterparts"
        
        # Generate word cloud
        wordcloud = WordCloud(width=800, height=400, background_color='white', 
                              colormap='viridis', max_words=50, 
                              contour_width=1, contour_color='steelblue').generate(text)
        
        # Display the word cloud
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
        
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "Search Documents":
    st.title("🔎 Search Documents")
    
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Semantic Search")
    
    search_query = st.text_input("Enter your search query", placeholder="e.g., termination notice period requirements")
    
    if st.button("Search", type="primary"):
        st.success("Search completed!")
        
        # Sample search results
        st.markdown("### Search Results")
        
        # Result 1
        st.markdown('<div style="padding:15px; background-color:#f8fafc; border:1px solid #e2e8f0; border-radius:5px; margin-bottom:15px;">'
                   '<h4 style="margin-top:0;">Employment Agreement (Section 5)</h4>'
                   '<p><mark>This Agreement may be terminated by either party with thirty (30) days written notice.</mark> '
                   'The Company may terminate the Employee's employment immediately for Cause...</p>'
                   '<p><strong>Relevance Score:</strong> 95%</p>'
                   '</div>', unsafe_allow_html=True)
        
        # Result 2
        st.markdown('<div style="padding:15px; background-color:#f8fafc; border:1px solid #e2e8f0; border-radius:5px; margin-bottom:15px;">'
                   '<h4 style="margin-top:0;">Service Agreement (Section 12)</h4>'
                   '<p>Either party may terminate this Agreement for convenience upon <mark>sixty (60) days prior written notice</mark> '
                   'to the other party. In the event of termination, the Service Provider shall be paid for services performed up to the termination date.</p>'
                   '<p><strong>Relevance Score:</strong> 82%</p>'
                   '</div>', unsafe_allow_html=True)
        
        # Result 3
        st.markdown('<div style="padding:15px; background-color:#f8fafc; border:1px solid #e2e8f0; border-radius:5px; margin-bottom:15px;">'
                   '<h4 style="margin-top:0;">Consulting Agreement (Section 8.2)</h4>'
                   '<p>The Agreement may be terminated by the Client without cause upon <mark>fifteen (15) days written notice</mark> '
                   'to the Consultant, or by the Consultant upon thirty (30) days written notice to the Client.</p>'
                   '<p><strong>Relevance Score:</strong> 78%</p>'
                   '</div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Search history
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Recent Searches")
    
    history = [
        "termination notice period requirements",
        "confidentiality clause examples",
        "compensation terms",
        "intellectual property rights",
        "governing law jurisdiction"
    ]
    
    for search_term in history:
        st.markdown(f"- {search_term}")
    
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
        - NetworkX
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
    **Email:** [yourname@example.com](mailto:yourname@example.com)  
    **GitHub:** [github.com/yourusername](https://github.com/yourusername)  
    """)
    
    st.markdown("</div>", unsafe_allow_html=True)
