#!/usr/bin/env python3
"""
LoanSathi Personal - Main Streamlit Application
Local loan eligibility and credit analysis tool
"""

import streamlit as st
from pathlib import Path
import sys
import logging
from datetime import datetime

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from logger import setup_logger
from config import config
from database.connection import DatabaseConnection
from database.operations import DatabaseOperations
from case_management.case_service import CaseService
from case_management.case_validator import CaseValidator

# Setup logging
logger = setup_logger('loansathi_app')

# Page configuration
st.set_page_config(
    page_title="LoanSathi Personal",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77d4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        padding: 1rem;
        border-radius: 0.5rem;
        color: #155724;
    }
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        padding: 1rem;
        border-radius: 0.5rem;
        color: #721c24;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        padding: 1rem;
        border-radius: 0.5rem;
        color: #856404;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    """Initialize Streamlit session state"""
    if 'db_connection' not in st.session_state:
        # Setup database
        data_dir = config.DATA_DIR
        global_db = data_dir / "global.db"
        db_conn = DatabaseConnection(global_db)
        db_conn.connect()
        db_conn.create_tables()
        
        st.session_state.db_connection = db_conn
        st.session_state.db_operations = DatabaseOperations(db_conn)
        st.session_state.case_service = CaseService(st.session_state.db_operations, data_dir)
    
    if 'current_case_id' not in st.session_state:
        st.session_state.current_case_id = None
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    
    if 'show_notification' not in st.session_state:
        st.session_state.show_notification = None

def show_notification(message: str, notification_type: str = 'success'):
    """Display a notification to user"""
    if notification_type == 'success':
        st.success(message)
    elif notification_type == 'error':
        st.error(message)
    elif notification_type == 'warning':
        st.warning(message)
    else:
        st.info(message)

def create_sidebar_navigation():
    """Create sidebar navigation menu"""
    with st.sidebar:
        st.markdown("<div class='main-header'>💰 LoanSathi</div>", unsafe_allow_html=True)
        st.markdown("<div class='sub-header'>Personal Edition v0.1.0</div>", unsafe_allow_html=True)
        
        st.divider()
        
        # Navigation menu
        st.subheader("Navigation")
        
        nav_options = {
            "🏠 Home": "home",
            "📋 Cases": "cases",
            "📄 Documents": "documents",
            "📊 Bank Analysis": "bank_analysis",
            "💰 Financials": "financials",
            "💵 Eligibility": "eligibility",
            "⚠️ Risk & Score": "risk_score",
            "🤖 Credit Officer": "credit_officer",
            "📈 Reports": "reports",
            "⚙️ Settings": "settings",
        }
        
        for label, page in nav_options.items():
            if st.button(label, key=f"nav_{page}", use_container_width=True):
                st.session_state.current_page = page
                st.rerun()
        
        st.divider()
        
        # Current case info
        if st.session_state.current_case_id:
            st.subheader("Current Case")
            try:
                case = st.session_state.case_service.get_case(st.session_state.current_case_id)
                if case:
                    st.info(f"📌 **{case['client_name']}**\n\nCase ID: {case['case_id']}")
                    if st.button("Clear Selection", use_container_width=True):
                        st.session_state.current_case_id = None
                        st.rerun()
            except Exception as e:
                logger.error(f"Error loading case: {e}")
        else:
            st.info("📌 No case selected. Go to Cases to create or select one.")
        
        st.divider()
        
        # Application info
        st.markdown("---")
        st.caption(f"**LoanSathi Personal**  \nVersion: {config.get('version', '0.1.0')}  \nAll data stays local on your computer.  \nNo cloud. No login. No subscription.")

def render_home_page():
    """Render home/dashboard page"""
    st.markdown("<div class='main-header'>Welcome to LoanSathi Personal</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Local Loan Eligibility & Credit Analysis Tool</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Cases", len(st.session_state.case_service.list_cases()))
    
    with col2:
        active_cases = len(st.session_state.case_service.list_cases('active'))
        st.metric("Active Cases", active_cases)
    
    with col3:
        inactive_cases = len(st.session_state.case_service.list_cases('inactive'))
        st.metric("Closed Cases", inactive_cases)
    
    st.divider()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Quick Start")
        st.markdown("""
        1. **Create a Case** - Go to Cases and create a new loan case
        2. **Upload Documents** - Upload bank statements and financial documents
        3. **Review Extraction** - Verify extracted data
        4. **Run Analysis** - Calculate eligibility and credit score
        5. **Generate Report** - Create professional PDF/Excel reports
        """)
    
    with col2:
        st.subheader("Key Features")
        st.markdown("""
        ✅ **100% Local** - All data stays on your laptop  
        ✅ **No Login** - Personal edition, no authentication  
        ✅ **Offline** - Works without internet connection  
        ✅ **Professional** - Bank-quality analysis and reporting  
        ✅ **Configurable** - Customize thresholds and assumptions  
        ✅ **Audit Trail** - Complete tracking of all actions  
        """)
    
    st.divider()
    
    st.subheader("Recent Cases")
    
    cases = st.session_state.case_service.list_cases('active')
    
    if cases:
        # Display recent cases
        for case in sorted(cases, key=lambda x: x['created_at'], reverse=True)[:5]:
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                st.write(f"**{case['client_name']}**")
                st.caption(f"{case['case_id']}")
            with col2:
                st.write(f"₹ {case['requested_amount']:,.0f}")
                st.caption(f"{case['loan_purpose']}")
            with col3:
                if st.button("Select", key=f"select_{case['case_id']}"):
                    st.session_state.current_case_id = case['case_id']
                    st.rerun()
    else:
        st.info("No active cases yet. Go to Cases to create one.")

def render_cases_page():
    """Render cases management page"""
    st.markdown("<div class='main-header'>Case Management</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["Active Cases", "New Case", "Case Actions"])
    
    with tab1:
        st.subheader("Active Cases")
        cases = st.session_state.case_service.list_cases('active')
        
        if cases:
            for case in sorted(cases, key=lambda x: x['created_at'], reverse=True):
                with st.container(border=True):
                    col1, col2, col3, col4 = st.columns([2, 2, 1.5, 1])
                    
                    with col1:
                        st.write(f"**{case['client_name']}**")
                        st.caption(f"Case: {case['case_id']}")
                    
                    with col2:
                        st.write(f"Amount: ₹ {case['requested_amount']:,.0f}")
                        st.caption(f"Tenure: {case['requested_tenure_months']} months")
                    
                    with col3:
                        st.write(f"Purpose: {case['loan_purpose']}")
                        st.caption(f"Constitution: {case['constitution']}")
                    
                    with col4:
                        if st.button("Open", key=f"open_{case['case_id']}"):
                            st.session_state.current_case_id = case['case_id']
                            show_notification(f"Case {case['case_id']} selected", 'success')
                            st.rerun()
        else:
            st.info("No active cases. Create a new case below.")
    
    with tab2:
        st.subheader("Create New Case")
        
        col1, col2 = st.columns(2)
        
        with col1:
            client_name = st.text_input("Client Name *", placeholder="e.g., Raj Kumar")
            pan = st.text_input("PAN (Optional)", placeholder="AAAAA0000A")
            business_name = st.text_input("Business Name (Optional)", placeholder="e.g., Kumar Enterprises")
            constitution = st.selectbox("Constitution *", CaseValidator.VALID_CONSTITUTIONS)
        
        with col2:
            loan_purpose = st.selectbox("Loan Purpose *", CaseValidator.VALID_LOAN_PURPOSES)
            requested_amount = st.number_input("Requested Amount (INR) *", min_value=0.0, step=10000.0, format="%f")
            requested_tenure = st.number_input("Requested Tenure (Months) *", min_value=1, max_value=360, step=1)
            interest_rate = st.number_input("Expected Interest Rate (%)", min_value=0.0, max_value=50.0, step=0.5, value=config.loan_assumptions.get('interest_rate', 12.0))
        
        industry = st.text_input("Industry (Optional)", placeholder="e.g., Manufacturing")
        location = st.text_input("Location (Optional)", placeholder="e.g., Mumbai")
        existing_banker = st.text_input("Existing Banker (Optional)", placeholder="e.g., HDFC Bank")
        notes = st.text_area("Notes", placeholder="Any additional information...")
        
        if st.button("Create Case", type="primary", use_container_width=True):
            # Validate input
            case_data = {
                'client_name': client_name,
                'pan_identifier': pan if pan else None,
                'business_name': business_name if business_name else None,
                'constitution': constitution,
                'industry': industry if industry else None,
                'location': location if location else None,
                'existing_banker': existing_banker if existing_banker else None,
                'loan_purpose': loan_purpose,
                'requested_amount': requested_amount,
                'requested_tenure_months': requested_tenure,
                'expected_interest_rate': interest_rate,
                'notes': notes if notes else None,
            }
            
            is_valid, errors = CaseValidator.validate_case_data(case_data)
            
            if is_valid:
                try:
                    case_id = st.session_state.case_service.create_case(case_data)
                    st.session_state.current_case_id = case_id
                    show_notification(f"✅ Case created successfully! Case ID: {case_id}", 'success')
                    st.rerun()
                except Exception as e:
                    logger.error(f"Error creating case: {e}")
                    show_notification(f"❌ Error creating case: {str(e)}", 'error')
            else:
                for error in errors:
                    st.error(error)
    
    with tab3:
        st.subheader("Case Actions")
        
        if st.session_state.current_case_id:
            case = st.session_state.case_service.get_case(st.session_state.current_case_id)
            if case:
                st.info(f"Selected: {case['client_name']} ({st.session_state.current_case_id})")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if st.button("📋 View Details", use_container_width=True):
                        st.session_state.current_page = 'case_details'
                        st.rerun()
                
                with col2:
                    if st.button("❌ Close Case", use_container_width=True):
                        if st.session_state.case_service.close_case(st.session_state.current_case_id):
                            show_notification("Case closed successfully", 'success')
                            st.session_state.current_case_id = None
                            st.rerun()
        else:
            st.warning("Please select a case first.")

def render_placeholder_page(page_name: str):
    """Render a placeholder page for future development"""
    st.markdown(f"<div class='main-header'>{page_name}</div>", unsafe_allow_html=True)
    st.info(f"🚧 {page_name} is coming in the next phase of development.")
    st.markdown("""
    This module is planned for Phase 2-9 of LoanSathi development.
    Check back soon!
    """)

def main():
    """Main application entry point"""
    # Initialize session state
    init_session_state()
    
    # Create sidebar navigation
    create_sidebar_navigation()
    
    # Route to appropriate page
    if st.session_state.current_page == 'home':
        render_home_page()
    elif st.session_state.current_page == 'cases':
        render_cases_page()
    elif st.session_state.current_page == 'documents':
        render_placeholder_page("Document Management (Phase 2)")
    elif st.session_state.current_page == 'bank_analysis':
        render_placeholder_page("Bank Statement Analysis (Phase 3)")
    elif st.session_state.current_page == 'financials':
        render_placeholder_page("Financial Data Module (Phase 4)")
    elif st.session_state.current_page == 'eligibility':
        render_placeholder_page("Loan Eligibility Engine (Phase 5)")
    elif st.session_state.current_page == 'risk_score':
        render_placeholder_page("Risk & Credit Scoring (Phase 6)")
    elif st.session_state.current_page == 'credit_officer':
        render_placeholder_page("AI Credit Officer Assessment (Phase 7)")
    elif st.session_state.current_page == 'reports':
        render_placeholder_page("Reporting Module (Phase 8)")
    elif st.session_state.current_page == 'settings':
        render_placeholder_page("Settings & Configuration (Phase 9)")
    else:
        render_home_page()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        st.error(f"An error occurred: {str(e)}")
