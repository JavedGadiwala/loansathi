#!/usr/bin/env python3
"""
Global Configuration Manager
Loads and manages all application settings from config files
"""

import json
import os
from pathlib import Path
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)

class Config:
    """Application configuration manager"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    CONFIG_DIR = DATA_DIR / "config"
    CASES_DIR = DATA_DIR / "cases"
    BACKUPS_DIR = DATA_DIR / "backups"
    
    # Ensure directories exist
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CASES_DIR.mkdir(parents=True, exist_ok=True)
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Configuration file paths
    APP_SETTINGS_FILE = CONFIG_DIR / "app_settings.json"
    CLASSIFICATION_RULES_FILE = CONFIG_DIR / "classification_rules.json"
    BANK_FORMATS_FILE = CONFIG_DIR / "bank_formats.json"
    DEFAULT_ASSUMPTIONS_FILE = CONFIG_DIR / "default_assumptions.json"
    
    # Default settings
    DEFAULT_SETTINGS = {
        "app_name": "LoanSathi Personal",
        "version": "0.1.0",
        "currency": "INR",
        "date_format": "DD-MMM-YYYY",
        "number_format": "#,##,###.00",
        "timezone": "Asia/Kolkata",
        "language": "en",
        "theme": "light",
    }
    
    DEFAULT_LOAN_ASSUMPTIONS = {
        "interest_rate": 12.0,
        "default_tenure_months": 60,
        "processing_fee_percent": 1.0,
        "documentation_required": True,
    }
    
    DEFAULT_RISK_THRESHOLDS = {
        "dscr_threshold_minimum": 1.25,
        "foir_threshold_maximum": 0.50,
        "low_balance_threshold": 50000,
        "high_cash_dependency_ratio": 0.60,
        "bounce_frequency_threshold": 3,
        "od_cc_utilization_threshold": 0.80,
        "turnover_variance_threshold": 0.25,
    }
    
    DEFAULT_CREDIT_SCORE_WEIGHTS = {
        "repayment_capacity": 30,
        "banking_behavior": 25,
        "cash_flow_quality": 15,
        "leverage": 15,
        "documentation_quality": 15,
    }
    
    def __init__(self):
        """Initialize configuration loader"""
        self.settings = self._load_settings()
        self.loan_assumptions = self._load_loan_assumptions()
        self.risk_thresholds = self._load_risk_thresholds()
        self.credit_score_weights = self._load_credit_score_weights()
        self.classification_rules = self._load_classification_rules()
        self.bank_formats = self._load_bank_formats()
    
    def _load_settings(self) -> Dict[str, Any]:
        """Load app settings from JSON or use defaults"""
        if self.APP_SETTINGS_FILE.exists():
            try:
                with open(self.APP_SETTINGS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading app settings: {e}. Using defaults.")
                return self.DEFAULT_SETTINGS.copy()
        else:
            self._save_settings(self.DEFAULT_SETTINGS)
            return self.DEFAULT_SETTINGS.copy()
    
    def _load_loan_assumptions(self) -> Dict[str, Any]:
        """Load loan assumptions from JSON or use defaults"""
        if self.DEFAULT_ASSUMPTIONS_FILE.exists():
            try:
                with open(self.DEFAULT_ASSUMPTIONS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading loan assumptions: {e}. Using defaults.")
                return self.DEFAULT_LOAN_ASSUMPTIONS.copy()
        else:
            self._save_json_file(self.DEFAULT_ASSUMPTIONS_FILE, self.DEFAULT_LOAN_ASSUMPTIONS)
            return self.DEFAULT_LOAN_ASSUMPTIONS.copy()
    
    def _load_risk_thresholds(self) -> Dict[str, Any]:
        """Load risk thresholds from JSON or use defaults"""
        return self._load_settings().get("risk_thresholds", self.DEFAULT_RISK_THRESHOLDS.copy())
    
    def _load_credit_score_weights(self) -> Dict[str, Any]:
        """Load credit score weights from JSON or use defaults"""
        return self._load_settings().get("credit_score_weights", self.DEFAULT_CREDIT_SCORE_WEIGHTS.copy())
    
    def _load_classification_rules(self) -> Dict[str, Any]:
        """Load transaction classification rules"""
        if self.CLASSIFICATION_RULES_FILE.exists():
            try:
                with open(self.CLASSIFICATION_RULES_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading classification rules: {e}")
                return {}
        else:
            default_rules = self._get_default_classification_rules()
            self._save_json_file(self.CLASSIFICATION_RULES_FILE, default_rules)
            return default_rules
    
    def _load_bank_formats(self) -> Dict[str, Any]:
        """Load bank format detection rules"""
        if self.BANK_FORMATS_FILE.exists():
            try:
                with open(self.BANK_FORMATS_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Error loading bank formats: {e}")
                return {}
        else:
            default_formats = self._get_default_bank_formats()
            self._save_json_file(self.BANK_FORMATS_FILE, default_formats)
            return default_formats
    
    @staticmethod
    def _get_default_classification_rules() -> Dict[str, Any]:
        """Default transaction classification keyword rules"""
        return {
            "salary": {"keywords": ["salary", "wages", "payroll", "epfo"], "category": "Salary", "type": "income"},
            "cash_deposit": {"keywords": ["cash deposit", "cash in", "atm"], "category": "Cash Deposit", "type": "internal"},
            "cheque_deposit": {"keywords": ["cheque", "chq"], "category": "Cheque Deposit", "type": "income"},
            "emi_payment": {"keywords": ["emi", "loan payment"], "category": "EMI Payment", "type": "obligation"},
            "upi_transfer": {"keywords": ["upi", "gpay", "paytm"], "category": "UPI Transfer", "type": "transfer"},
        }
    
    @staticmethod
    def _get_default_bank_formats() -> Dict[str, Any]:
        """Default bank format detection patterns"""
        return {
            "HDFC": {"keywords": ["hdfc"], "date_format": "DD/MM/YYYY"},
            "ICICI": {"keywords": ["icici"], "date_format": "DD/MM/YYYY"},
            "SBI": {"keywords": ["sbi"], "date_format": "DD-MMM-YYYY"},
            "Axis": {"keywords": ["axis"], "date_format": "DD/MM/YYYY"},
        }
    
    def _save_settings(self, settings: Dict[str, Any]) -> None:
        """Save settings to JSON file"""
        self._save_json_file(self.APP_SETTINGS_FILE, settings)
    
    @staticmethod
    def _save_json_file(filepath: Path, data: Dict[str, Any]) -> None:
        """Save dictionary to JSON file"""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved configuration to {filepath}")
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value and save"""
        self.settings[key] = value
        self._save_settings(self.settings)
    
    def reload(self) -> None:
        """Reload all configurations from disk"""
        self.settings = self._load_settings()
        self.loan_assumptions = self._load_loan_assumptions()
        self.risk_thresholds = self._load_risk_thresholds()
        logger.info("Configuration reloaded")

config = Config()
