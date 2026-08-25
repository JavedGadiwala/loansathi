# LoanSathi Personal

**Local Loan Eligibility & Credit Analysis Tool for Chartered Accountants in India**

## Overview

LoanSathi Personal is a desktop application for analyzing loan eligibility and credit risk. It processes financial and banking documents, extracts data, performs quantitative analysis, calculates repayment capacity, and generates professional PDF/Excel reports.

**Key Features:**
- 🏠 **100% Local** - No cloud, no login, no subscription required
- 📁 **Offline-First** - Works without internet connection
- 🔒 **Private** - All client data stays on your Windows laptop
- 📊 **Comprehensive Analysis** - Bank statements, financials, ITR, GST
- 📈 **Credit Scoring** - Explainable 0-100 credit rating
- 📄 **Professional Reports** - PDF & Excel export

## Quick Start

### Installation (Windows)

1. **Download & Extract**
   ```
   Download loansathi-release.zip
   Extract to: C:\LoanSathi\
   ```

2. **Run the Application**
   ```
   Double-click: Start LoanSathi.exe
   Browser will open automatically
   ```

3. **Create Your First Case**
   - Click "New Case"
   - Enter client name and loan details
   - Upload bank statements
   - Run analysis
   - Generate report

### System Requirements

- **Windows 10 or later** (64-bit)
- **No Python installation needed** (bundled with app)
- **500 MB free disk space** (minimum)
- **Internet not required** (core functionality is offline)

## Project Structure

```
loansathi/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── setup.py                       # Installation configuration
├── Start LoanSathi.bat            # Windows batch launcher
├── Start LoanSathi.exe            # Compiled Windows executable (Phase 10)
│
├── src/
│   ├── __init__.py
│   ├── app.py                     # Main Streamlit application
│   ├── config.py                  # Global settings & configuration
│   ├── logger.py                  # Logging setup
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py          # SQLite connection & initialization
│   │   ├── models.py              # Database schema definitions
│   │   ├── operations.py          # CRUD operations for all entities
│   │   └── migrations.py          # Database schema upgrades
│   │
│   ├── case_management/
│   │   ├── __init__.py
│   │   ├── case_service.py        # Case creation, retrieval, update
│   │   ├── case_backup.py         # Case backup/restore/export
│   │   └── case_validator.py      # Input validation
│   │
│   ├── document_ingestion/
│   │   ├── __init__.py
│   │   ├── document_handler.py    # File upload & storage
│   │   ├── pdf_extractor.py       # PDF parsing (pdfplumber)
│   │   ├── excel_extractor.py     # Excel/CSV parsing
│   │   ├── ocr_engine.py          # OCR for scanned PDFs (optional)
│   │   ├── document_classifier.py # Detect document type & bank
│   │   └── extraction_preview.py  # Display & review extraction
│   │
│   ├── transaction_engine/
│   │   ├── __init__.py
│   │   ├── transaction_model.py   # Standardized transaction schema
│   │   ├── transaction_parser.py  # Parse bank statements to transactions
│   │   ├── transaction_classifier.py # Categorize transactions
│   │   ├── duplicate_detector.py  # Find & flag duplicates
│   │   └── transaction_storage.py # Store & retrieve transactions
│   │
│   ├── bank_analysis/
│   │   ├── __init__.py
│   │   ├── statement_analyzer.py  # Monthly aggregation & metrics
│   │   ├── cc_od_analyzer.py      # Credit card/OD analysis
│   │   ├── trend_calculator.py    # 3/6/12/24-month trends
│   │   └── bank_report_builder.py # Generate banking analysis report
│   │
│   ├── financial_module/
│   │   ├── __init__.py
│   │   ├── financial_data.py      # P&L, Balance Sheet, Cash Flow models
│   │   ├── itr_parser.py          # ITR data entry/parsing
│   │   ├── gst_parser.py          # GST data entry/parsing
│   │   ├── reconciliation.py      # Bank vs Reported turnover comparison
│   │   └── financial_validator.py # Data quality checks
│   │
│   ├── eligibility_engine/
│   │   ├── __init__.py
│   │   ├── emi_calculator.py      # EMI calculation (reducing balance)
│   │   ├── dscr_calculator.py     # Debt Service Coverage Ratio
│   │   ├── foir_calculator.py     # Fixed Obligation to Income Ratio
│   │   ├── eligibility_methods.py # Multiple eligibility methods
│   │   ├── turnover_based.py      # Working capital based on bank turnover
│   │   └── ltv_calculator.py      # LTV for secured lending (future)
│   │
│   ├── risk_scoring/
│   │   ├── __init__.py
│   │   ├── risk_flags.py          # Detect & score risk flags
│   │   ├── credit_score.py        # 0-100 credit rating engine
│   │   ├── score_weights.py       # Configurable score factors
│   │   └── risk_report.py         # Risk assessment narrative
│   │
│   ├── credit_officer/
│   │   ├── __init__.py
│   │   ├── ai_officer.py          # Rule-based credit assessment
│   │   ├── narrative_builder.py   # Generate credit officer narrative
│   │   ├── recommendation.py      # Strong/Acceptable/Caution/Weak/Decline
│   │   └── llm_integration.py     # Future: Optional LLM integration
│   │
│   ├── reporting/
│   │   ├── __init__.py
│   │   ├── pdf_generator.py       # PDF report (ReportLab)
│   │   ├── excel_generator.py     # Excel export (openpyxl)
│   │   ├── report_templates.py    # Report sections & formatting
│   │   └── report_storage.py      # Store generated reports
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── pages/
│   │   │   ├── home.py            # Dashboard & summary
│   │   │   ├── cases.py           # Case management UI
│   │   │   ├── documents.py       # Document upload & review
│   │   │   ├── bank_analysis.py   # Bank statement analysis view
│   │   │   ├── financials.py      # Financial/ITR/GST entry
│   │   │   ├── eligibility.py     # Eligibility calculations & methods
│   │   │   ├── risk_score.py      # Risk flags & credit score
│   │   │   ├── credit_officer.py  # AI Credit Officer assessment
│   │   │   ├── reports.py         # Generate & download reports
│   │   │   └── settings.py        # Application settings
│   │   │
│   │   ├── components.py          # Reusable UI components
│   │   ├── styles.py              # CSS/formatting utilities
│   │   └── helpers.py             # UI helper functions
│   │
│   └── utils/
│       ├── __init__.py
│       ├── validators.py          # Input validation
│       ├── formatters.py          # Number/date formatting
│       ├── constants.py           # Application constants
│       ├── indian_banking.py      # Indian bank detection, account types
│       ├── date_parser.py         # Flexible date parsing
│       └── error_handler.py       # Error handling & logging
│
├── data/
│   ├── cases/                     # Case data (auto-created)
│   │   └── CASE_ID_20250101/
│   │       ├── case.db            # Case metadata & transactions
│   │       ├── documents/         # Original uploaded files
│   │       ├── extractions/       # Parsed extraction previews
│   │       └── reports/           # Generated reports
│   │
│   ├── config/
│   │   ├── app_settings.json      # User settings (thresholds, weights, etc.)
│   │   ├── classification_rules.json # Transaction classification rules
│   │   ├── bank_formats.json      # Bank detection & parsing rules
│   │   └── default_assumptions.json # Default loan assumptions
│   │
│   └── backups/                   # Auto-backups (optional)
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                # Pytest fixtures
│   ├── test_emi_calculator.py     # EMI calculation tests
│   ├── test_dscr_calculator.py    # DSCR tests
│   ├── test_foir_calculator.py    # FOIR tests
│   ├── test_transaction_parser.py # Transaction parsing tests
│   ├── test_duplicate_detector.py # Duplicate detection tests
│   ├── test_credit_score.py       # Score calculation tests
│   ├── test_case_operations.py    # Case CRUD tests
│   ├── test_pdf_extraction.py     # PDF parsing tests
│   └── fixtures/
│       ├── sample_bank_statement.pdf
│       ├── sample_financial.xlsx
│       └── sample_transactions.csv
│
├── docs/
│   ├── INSTALLATION.md            # Detailed Windows setup
│   ├── USER_GUIDE.md              # How to use the application
│   ├── CALCULATION_GUIDE.md       # Formulas & methodologies
│   ├── DATABASE_SCHEMA.md         # Data model reference
│   ├── API_REFERENCE.md           # Module documentation
│   └── TROUBLESHOOTING.md         # Common issues & fixes
│
└── build/
    └── (Windows executable build output - Phase 10)
```

## Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Framework** | Python 3.12+ | Core logic |
| **UI** | Streamlit | Browser-based interface |
| **Database** | SQLite | Local persistent storage |
| **PDF Extraction** | pdfplumber | Bank statement text/table parsing |
| **Excel/CSV** | openpyxl, Pandas | Import/export |
| **OCR** | Tesseract (optional) | Scanned document processing |
| **PDF Reports** | ReportLab | Professional PDF generation |
| **Charts** | Plotly | Interactive analysis visualizations |
| **Packaging** | PyInstaller | Windows .exe bundling |

## Configuration

All settings are stored in `data/config/app_settings.json` (editable):

```json
{
  "currency": "INR",
  "date_format": "DD-MMM-YYYY",
  "loan_assumptions": {
    "interest_rate": 12.0,
    "default_tenure_months": 60
  },
  "dscr_threshold": 1.25,
  "foir_threshold": 0.50,
  "credit_score_weights": {
    "repayment_capacity": 30,
    "banking_behavior": 25,
    "cash_flow_quality": 15,
    "leverage": 15,
    "documentation": 15
  },
  "risk_flags": {
    "low_balance_threshold": 50000,
    "high_cash_dependency": 0.6,
    "bounce_frequency_threshold": 3
  }
}
```

## Workflow Summary

1. **Create Case** → Enter client & loan details
2. **Upload Documents** → Bank statements, financials, ITR, GST
3. **Review Extraction** → Verify and correct parsed data
4. **Run Analysis** → Calculate banking metrics, eligibility, risk, score
5. **Generate Report** → Export PDF/Excel
6. **Backup Case** → One-click local ZIP backup

## Development Phases

| Phase | Deliverable | Status |
|-------|-------------|--------|
| 1 | Project skeleton, case management, navigation | 🔄 IN PROGRESS |
| 2 | Document upload/extraction, transaction model | ⏳ Planned |
| 3 | Bank statement analysis, dashboard | ⏳ Planned |
| 4 | Financial/ITR/GST data module | ⏳ Planned |
| 5 | Eligibility & EMI/DSCR/FOIR engine | ⏳ Planned |
| 6 | Risk flags & 0-100 credit score | ⏳ Planned |
| 7 | AI Credit Officer narrative | ⏳ Planned |
| 8 | PDF/Excel reporting | ⏳ Planned |
| 9 | Audit trail, backup, settings | ⏳ Planned |
| 10 | Testing, packaging, Windows deployment | ⏳ Planned |

## Data Security & Privacy

- ✅ **No cloud storage** - All data remains on your laptop
- ✅ **No login required** - Personal edition, no authentication
- ✅ **Original files preserved** - Never destructively modified
- ✅ **Local backup** - One-click case export as ZIP
- ✅ **Audit trail** - Track all uploads, changes, reviews
- ✅ **No external API calls** - Core functionality fully offline

## Support & Documentation

- See `docs/` folder for detailed guides
- Check `TROUBLESHOOTING.md` for common issues
- All calculations are documented with formulas and assumptions

## License

Proprietary - Personal use only.

---

**Version:** 0.1.0 (Phase 1)  
**Last Updated:** August 2026  
**Status:** Under Active Development
