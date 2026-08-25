#!/usr/bin/env python3
"""
Transaction Parser - Parse and standardize transactions
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import re

logger = logging.getLogger(__name__)

class TransactionParser:
    """Parse and standardize extracted transactions"""
    
    def __init__(self):
        """Initialize transaction parser"""
        pass
    
    def parse_transaction(self, raw_transaction: Dict[str, Any], bank: Optional[str] = None) -> Dict[str, Any]:
        """
        Parse a raw transaction into standardized format
        
        Args:
            raw_transaction: Raw transaction dictionary
            bank: Bank name for bank-specific parsing
        
        Returns:
            Standardized transaction dictionary
        """
        transaction = {
            'transaction_id': None,
            'date': None,
            'value_date': None,
            'narration': None,
            'reference_number': None,
            'debit': 0.0,
            'credit': 0.0,
            'balance': None,
            'transaction_type': 'Other',
            'category': 'Uncategorized',
            'counterparty': None,
            'confidence': 0.0,
        }
        
        try:
            # Parse date
            date = self._parse_date(raw_transaction.get('date', ''))
            if date:
                transaction['date'] = date
                transaction['value_date'] = date
            
            # Parse amounts
            debit = self._parse_amount(raw_transaction.get('debit', 0))
            credit = self._parse_amount(raw_transaction.get('credit', 0))
            transaction['debit'] = debit
            transaction['credit'] = credit
            
            # Parse narration
            narration = str(raw_transaction.get('narration', '')).strip()
            transaction['narration'] = narration
            
            # Extract reference number
            ref_num = self._extract_reference_number(narration)
            transaction['reference_number'] = ref_num
            
            # Parse balance
            balance = self._parse_amount(raw_transaction.get('balance', None))
            if balance is not None:
                transaction['balance'] = balance
            
            # Determine transaction type
            tx_type = self._determine_transaction_type(narration, debit, credit)
            transaction['transaction_type'] = tx_type
            
            # Categorize transaction
            category = self._categorize_transaction(narration, tx_type)
            transaction['category'] = category
            
            # Extract counterparty
            counterparty = self._extract_counterparty(narration)
            transaction['counterparty'] = counterparty
            
            # Calculate confidence
            confidence = self._calculate_confidence(transaction)
            transaction['confidence'] = confidence
            
            logger.debug(f"Parsed transaction: {narration[:50]}... ({category})")
            return transaction
        
        except Exception as e:
            logger.error(f"Error parsing transaction: {e}")
            return transaction
    
    def parse_transactions(self, raw_transactions: List[Dict]) -> List[Dict]:
        """
        Parse multiple transactions
        
        Args:
            raw_transactions: List of raw transactions
        
        Returns:
            List of standardized transactions
        """
        parsed = []
        for raw_tx in raw_transactions:
            if raw_tx:
                parsed.append(self.parse_transaction(raw_tx))
        
        logger.info(f"Parsed {len(parsed)} transactions")
        return parsed
    
    @staticmethod
    def _parse_date(date_str: str) -> Optional[str]:
        """
        Parse date string into standard format (YYYY-MM-DD)
        
        Args:
            date_str: Date string
        
        Returns:
            Formatted date or None
        """
        if not date_str:
            return None
        
        date_str = str(date_str).strip()
        
        # Try common formats
        formats = [
            '%d/%m/%Y', '%d-%m-%Y', '%d.%m.%Y',  # DD/MM/YYYY
            '%d/%m/%y', '%d-%m-%y', '%d.%m.%y',   # DD/MM/YY
            '%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d',   # YYYY-MM-DD
            '%d %b %Y', '%d %B %Y',                # DD MMM YYYY
            '%b %d, %Y', '%B %d, %Y',              # MMM DD, YYYY
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime('%Y-%m-%d')
            except ValueError:
                continue
        
        return None
    
    @staticmethod
    def _parse_amount(amount: Any) -> float:
        """
        Parse amount string/number into float
        
        Args:
            amount: Amount value
        
        Returns:
            Float amount or 0.0
        """
        if amount is None or amount == '':
            return 0.0
        
        try:
            amount_str = str(amount).strip()
            # Remove common separators
            amount_str = amount_str.replace(',', '').replace(' ', '')
            return float(amount_str)
        except (ValueError, AttributeError):
            return 0.0
    
    @staticmethod
    def _extract_reference_number(narration: str) -> Optional[str]:
        """
        Extract reference number from narration
        
        Args:
            narration: Transaction narration
        
        Returns:
            Reference number or None
        """
        if not narration:
            return None
        
        # Look for reference patterns
        patterns = [
            r'REF[#:]?\s*([A-Z0-9]{6,20})',
            r'UPI[:]?\s*([A-Z0-9@.]{6,30})',
            r'CHQ[#:]?\s*([0-9]{6,12})',
            r'TXN[#:]?\s*([A-Z0-9]{6,20})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, narration, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    @staticmethod
    def _determine_transaction_type(narration: str, debit: float, credit: float) -> str:
        """
        Determine transaction type
        
        Args:
            narration: Transaction narration
            debit: Debit amount
            credit: Credit amount
        
        Returns:
            Transaction type
        """
        narration_lower = narration.lower()
        
        # Categorize by narration keywords
        if any(kw in narration_lower for kw in ['salary', 'wages', 'payroll']):
            return 'Salary'
        elif any(kw in narration_lower for kw in ['cheque', 'chq', 'deposit']):
            return 'Cheque'
        elif any(kw in narration_lower for kw in ['upi', 'gpay', 'paytm', 'phonepay']):
            return 'UPI'
        elif any(kw in narration_lower for kw in ['neft', 'rtgs', 'imps']):
            return 'Fund Transfer'
        elif any(kw in narration_lower for kw in ['emi', 'loan', 'instalment']):
            return 'Loan Payment'
        elif any(kw in narration_lower for kw in ['charge', 'fee', 'commission']):
            return 'Fee'
        elif any(kw in narration_lower for kw in ['interest', 'dividend', 'income']):
            return 'Interest'
        elif credit > 0:
            return 'Deposit'
        elif debit > 0:
            return 'Withdrawal'
        else:
            return 'Other'
    
    @staticmethod
    def _categorize_transaction(narration: str, transaction_type: str) -> str:
        """
        Categorize transaction
        
        Args:
            narration: Transaction narration
            transaction_type: Transaction type
        
        Returns:
            Category
        """
        narration_lower = narration.lower()
        
        # Income categories
        if any(kw in narration_lower for kw in ['salary', 'wages', 'payroll']):
            return 'Salary'
        elif any(kw in narration_lower for kw in ['business', 'revenue', 'sales']):
            return 'Business Income'
        elif any(kw in narration_lower for kw in ['interest', 'dividend', 'profit']):
            return 'Investment Income'
        
        # Expense categories
        elif any(kw in narration_lower for kw in ['electricity', 'water', 'gas', 'broadband', 'internet']):
            return 'Utilities'
        elif any(kw in narration_lower for kw in ['rent', 'lease', 'property']):
            return 'Rent'
        elif any(kw in narration_lower for kw in ['tax', 'gst', 'itr', 'tds']):
            return 'Tax'
        elif any(kw in narration_lower for kw in ['emi', 'loan', 'instalment']):
            return 'Loan EMI'
        elif any(kw in narration_lower for kw in ['insurance', 'premium']):
            return 'Insurance'
        elif any(kw in narration_lower for kw in ['travel', 'flight', 'hotel', 'taxi']):
            return 'Travel'
        elif any(kw in narration_lower for kw in ['food', 'restaurant', 'grocery']):
            return 'Food & Groceries'
        
        # Transfers
        elif any(kw in narration_lower for kw in ['transfer', 'neft', 'rtgs', 'imps']):
            return 'Transfer'
        elif any(kw in narration_lower for kw in ['atm', 'withdrawal', 'cash']):
            return 'Cash Withdrawal'
        
        # Bank operations
        elif any(kw in narration_lower for kw in ['charge', 'fee', 'commission', 'penalty']):
            return 'Bank Charges'
        elif any(kw in narration_lower for kw in ['cheque', 'chq', 'clearing', 'rturn']):
            return 'Cheque Related'
        
        # Default
        else:
            return 'Other'
    
    @staticmethod
    def _extract_counterparty(narration: str) -> Optional[str]:
        """
        Extract counterparty from narration
        
        Args:
            narration: Transaction narration
        
        Returns:
            Counterparty name or None
        """
        if not narration or len(narration) < 3:
            return None
        
        # Remove common prefixes
        prefixes = ['to ', 'from ', 'via ', 'by ', 'for ']
        narration_lower = narration.lower()
        
        for prefix in prefixes:
            if narration_lower.startswith(prefix):
                counterparty = narration[len(prefix):].split('-')[0].split('/')[0].strip()
                if counterparty and len(counterparty) > 2:
                    return counterparty
        
        # Try to extract first meaningful word
        words = narration.split()
        if words and len(words[0]) > 2:
            return words[0]
        
        return None
    
    @staticmethod
    def _calculate_confidence(transaction: Dict) -> float:
        """
        Calculate confidence score for parsed transaction
        
        Args:
            transaction: Parsed transaction
        
        Returns:
            Confidence score (0-1)
        """
        confidence = 0.0
        
        # Has date
        if transaction['date']:
            confidence += 0.25
        
        # Has amount
        if transaction['debit'] > 0 or transaction['credit'] > 0:
            confidence += 0.25
        
        # Has narration
        if transaction['narration']:
            confidence += 0.25
        
        # Has categorization
        if transaction['category'] != 'Uncategorized':
            confidence += 0.15
        
        # Has counterparty
        if transaction['counterparty']:
            confidence += 0.10
        
        return min(1.0, confidence)
