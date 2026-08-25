#!/usr/bin/env python3
"""
Case Data Validation
Validates case input data
"""

from typing import Dict, Any, Tuple, List
import logging
import re

logger = logging.getLogger(__name__)

class CaseValidator:
    """Validator for case data"""
    
    VALID_CONSTITUTIONS = [
        'Individual',
        'Proprietorship',
        'Partnership',
        'LLP',
        'Company',
        'Other'
    ]
    
    VALID_LOAN_PURPOSES = [
        'Working Capital',
        'Term Loan',
        'Overdraft/CC',
        'LAP',
        'Business Expansion',
        'Other'
    ]
    
    @staticmethod
    def validate_case_data(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate complete case data
        
        Args:
            data: Case data dictionary
        
        Returns:
            (is_valid: bool, errors: List[str])
        """
        errors = []
        
        # Validate required fields
        if not data.get('client_name', '').strip():
            errors.append("Client name is required")
        
        if not data.get('loan_purpose', '').strip():
            errors.append("Loan purpose is required")
        
        # Validate optional fields if provided
        if data.get('requested_amount'):
            if not CaseValidator.is_valid_amount(data['requested_amount']):
                errors.append("Requested amount must be a positive number")
        
        if data.get('requested_tenure_months'):
            if not CaseValidator.is_valid_tenure(data['requested_tenure_months']):
                errors.append("Requested tenure must be between 1 and 360 months")
        
        if data.get('expected_interest_rate'):
            if not CaseValidator.is_valid_rate(data['expected_interest_rate']):
                errors.append("Interest rate must be between 0 and 50%")
        
        if data.get('pan_identifier'):
            if not CaseValidator.is_valid_pan(data['pan_identifier']):
                errors.append("Invalid PAN format")
        
        if data.get('constitution'):
            if data['constitution'] not in CaseValidator.VALID_CONSTITUTIONS:
                errors.append(f"Constitution must be one of {CaseValidator.VALID_CONSTITUTIONS}")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def is_valid_amount(amount: Any) -> bool:
        """Validate amount is positive number"""
        try:
            val = float(amount)
            return val > 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_valid_tenure(months: Any) -> bool:
        """Validate tenure is between 1-360 months"""
        try:
            val = int(months)
            return 1 <= val <= 360
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_valid_rate(rate: Any) -> bool:
        """Validate interest rate is between 0-50%"""
        try:
            val = float(rate)
            return 0 <= val <= 50
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_valid_pan(pan: str) -> bool:
        """Validate PAN format (Indian PAN)"""
        if not pan:
            return False
        # PAN format: AAAAA9999A
        pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$'
        return bool(re.match(pattern, pan.upper()))
