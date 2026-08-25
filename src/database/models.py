#!/usr/bin/env python3
"""
Database Schema Models
"""

SCHEMA = {
    "cases": """
        CREATE TABLE IF NOT EXISTS cases (
            case_id TEXT PRIMARY KEY,
            client_name TEXT NOT NULL,
            pan_identifier TEXT,
            business_name TEXT,
            constitution TEXT,
            industry TEXT,
            location TEXT,
            existing_banker TEXT,
            loan_purpose TEXT,
            requested_amount REAL,
            requested_tenure_months INTEGER,
            expected_interest_rate REAL,
            assessment_date TEXT,
            notes TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            status TEXT DEFAULT 'active'
        )
    """,
    
    "documents": """
        CREATE TABLE IF NOT EXISTS documents (
            document_id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL,
            file_name TEXT NOT NULL,
            file_type TEXT,
            document_type TEXT,
            file_path TEXT NOT NULL,
            file_size INTEGER,
            upload_date TEXT NOT NULL,
            extraction_status TEXT DEFAULT 'pending',
            extraction_confidence REAL,
            bank_name TEXT,
            account_number TEXT,
            statement_period_start TEXT,
            statement_period_end TEXT,
            notes TEXT,
            FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE
        )
    """,
    
    "transactions": """
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL,
            account_id TEXT,
            transaction_date TEXT NOT NULL,
            value_date TEXT,
            narration TEXT,
            reference_number TEXT,
            debit REAL DEFAULT 0,
            credit REAL DEFAULT 0,
            balance REAL,
            transaction_type TEXT,
            category TEXT,
            counterparty TEXT,
            source_file TEXT,
            source_page TEXT,
            confidence REAL,
            review_status TEXT DEFAULT 'unreviewed',
            is_manual_entry INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE
        )
    """,
    
    "financial_data": """
        CREATE TABLE IF NOT EXISTS financial_data (
            financial_id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL,
            financial_year TEXT,
            document_type TEXT,
            p_and_l_revenue REAL,
            p_and_l_gross_profit REAL,
            p_and_l_ebitda REAL,
            p_and_l_depreciation REAL,
            p_and_l_interest REAL,
            p_and_l_pbt REAL,
            p_and_l_pat REAL,
            bs_capital_net_worth REAL,
            bs_fixed_assets REAL,
            bs_current_assets REAL,
            bs_inventory REAL,
            bs_receivables REAL,
            bs_cash_bank REAL,
            bs_current_liabilities REAL,
            bs_loans_liabilities REAL,
            bs_creditors REAL,
            itr_income REAL,
            itr_turnover REAL,
            itr_tax_paid REAL,
            gst_turnover REAL,
            gst_tax_collected REAL,
            gst_tax_paid REAL,
            source_document TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE
        )
    """,
    
    "eligibility_calculations": """
        CREATE TABLE IF NOT EXISTS eligibility_calculations (
            calculation_id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL,
            method TEXT,
            principal_amount REAL,
            interest_rate REAL,
            tenure_months INTEGER,
            monthly_emi REAL,
            total_interest REAL,
            total_repayment REAL,
            dscr_value REAL,
            dscr_threshold REAL,
            foir_value REAL,
            foir_threshold REAL,
            eligible_amount REAL,
            calculation_date TEXT NOT NULL,
            notes TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE
        )
    """,
    
    "credit_scores": """
        CREATE TABLE IF NOT EXISTS credit_scores (
            score_id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL,
            overall_score REAL,
            repayment_capacity_score REAL,
            banking_behavior_score REAL,
            cash_flow_quality_score REAL,
            leverage_score REAL,
            documentation_quality_score REAL,
            score_date TEXT NOT NULL,
            calculation_details TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE
        )
    """,
    
    "risk_flags": """
        CREATE TABLE IF NOT EXISTS risk_flags (
            flag_id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL,
            flag_type TEXT,
            severity TEXT,
            description TEXT,
            detected_value REAL,
            threshold_value REAL,
            flag_date TEXT NOT NULL,
            acknowledged INTEGER DEFAULT 0,
            acknowledgement_comment TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE
        )
    """,
    
    "reports": """
        CREATE TABLE IF NOT EXISTS reports (
            report_id TEXT PRIMARY KEY,
            case_id TEXT NOT NULL,
            report_type TEXT,
            report_format TEXT,
            file_path TEXT,
            file_size INTEGER,
            generation_date TEXT NOT NULL,
            reviewer_name TEXT,
            review_date TEXT,
            review_comments TEXT,
            final_recommendation TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE
        )
    """,
    
    "audit_trail": """
        CREATE TABLE IF NOT EXISTS audit_trail (
            audit_id TEXT PRIMARY KEY,
            case_id TEXT,
            action TEXT NOT NULL,
            entity_type TEXT,
            entity_id TEXT,
            old_value TEXT,
            new_value TEXT,
            user_action TEXT,
            reason_for_change TEXT,
            action_date TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE SET NULL
        )
    """,
}
