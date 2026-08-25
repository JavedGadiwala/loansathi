#!/usr/bin/env python3
"""
Excel Extractor - Extract data from Excel and CSV files
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

try:
    import pandas as pd
except ImportError:
    pd = None

logger = logging.getLogger(__name__)

class ExcelExtractor:
    """Extract data from Excel and CSV files"""
    
    def __init__(self):
        """
        Initialize Excel extractor
        """
        if pd is None:
            logger.warning("pandas not installed. Excel extraction will not work.")
    
    def extract_from_excel(self, file_path: Path, sheet_name: Optional[str] = None) -> List[Dict]:
        """
        Extract data from Excel file
        
        Args:
            file_path: Path to Excel file
            sheet_name: Sheet name to extract (default: first sheet)
        
        Returns:
            List of dictionaries (rows)
        """
        if pd is None:
            logger.error("pandas not installed")
            return []
        
        try:
            # Read Excel file
            if sheet_name:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
            else:
                df = pd.read_excel(file_path)
            
            # Convert to list of dicts
            records = df.to_dict('records')
            
            logger.info(f"Extracted {len(records)} rows from {file_path.name}")
            return records
        
        except Exception as e:
            logger.error(f"Error extracting from Excel: {e}")
            return []
    
    def extract_from_csv(self, file_path: Path) -> List[Dict]:
        """
        Extract data from CSV file
        
        Args:
            file_path: Path to CSV file
        
        Returns:
            List of dictionaries (rows)
        """
        if pd is None:
            logger.error("pandas not installed")
            return []
        
        try:
            # Read CSV file
            df = pd.read_csv(file_path)
            
            # Convert to list of dicts
            records = df.to_dict('records')
            
            logger.info(f"Extracted {len(records)} rows from {file_path.name}")
            return records
        
        except Exception as e:
            logger.error(f"Error extracting from CSV: {e}")
            return []
    
    def get_sheet_names(self, file_path: Path) -> List[str]:
        """
        Get sheet names from Excel file
        
        Args:
            file_path: Path to Excel file
        
        Returns:
            List of sheet names
        """
        if pd is None:
            return []
        
        try:
            excel_file = pd.ExcelFile(file_path)
            return excel_file.sheet_names
        except Exception as e:
            logger.error(f"Error getting sheet names: {e}")
            return []
    
    def extract_bank_statement_data(self, file_path: Path) -> Dict[str, Any]:
        """
        Extract bank statement data from Excel/CSV
        
        Args:
            file_path: Path to Excel/CSV file
        
        Returns:
            Dictionary with extracted data
        """
        result = {
            'success': False,
            'bank_name': None,
            'account_number': None,
            'statement_period': None,
            'transactions': [],
            'confidence': 0.0,
            'raw_data': [],
            'errors': []
        }
        
        try:
            # Determine file type
            if file_path.suffix.lower() == '.csv':
                data = self.extract_from_csv(file_path)
            else:
                data = self.extract_from_excel(file_path)
            
            if not data:
                result['errors'].append("No data extracted")
                return result
            
            result['raw_data'] = data
            result['success'] = True
            result['confidence'] = 0.85  # Excel usually has better structure
            
            # Try to standardize transaction columns
            transactions = self._standardize_transactions(data)
            result['transactions'] = transactions
            
            logger.info(f"Extracted {len(transactions)} transactions from {file_path.name}")
            return result
        
        except Exception as e:
            logger.error(f"Error extracting bank statement: {e}")
            result['errors'].append(str(e))
            return result
    
    @staticmethod
    def _standardize_transactions(raw_data: List[Dict]) -> List[Dict]:
        """
        Standardize transaction column names from raw data
        
        Args:
            raw_data: Raw extracted data
        
        Returns:
            List of standardized transactions
        """
        transactions = []
        
        # Common column name patterns
        date_columns = ['date', 'transaction_date', 'txn_date', 'posted_date']
        debit_columns = ['debit', 'withdrawal', 'deducted', 'amount_out']
        credit_columns = ['credit', 'deposit', 'credited', 'amount_in']
        narration_columns = ['narration', 'description', 'reference', 'remarks']
        balance_columns = ['balance', 'closing_balance', 'available_balance']
        
        for row in raw_data:
            # Skip header rows or empty rows
            if not row or all(v is None or str(v).strip() == '' for v in row.values()):
                continue
            
            # Find matching columns
            date_val = None
            debit_val = None
            credit_val = None
            narration_val = None
            balance_val = None
            
            for col_name, col_val in row.items():
                col_lower = str(col_name).lower()
                
                if any(dc in col_lower for dc in date_columns) and not date_val:
                    date_val = col_val
                elif any(dc in col_lower for dc in debit_columns) and not debit_val:
                    debit_val = col_val
                elif any(dc in col_lower for dc in credit_columns) and not credit_val:
                    credit_val = col_val
                elif any(nc in col_lower for nc in narration_columns) and not narration_val:
                    narration_val = col_val
                elif any(bc in col_lower for bc in balance_columns) and not balance_val:
                    balance_val = col_val
            
            # Only add if has at least date and amount
            if date_val and (debit_val or credit_val):
                transactions.append({
                    'date': str(date_val),
                    'debit': float(debit_val) if debit_val and str(debit_val).replace('.', '').isdigit() else 0.0,
                    'credit': float(credit_val) if credit_val and str(credit_val).replace('.', '').isdigit() else 0.0,
                    'narration': str(narration_val) if narration_val else '',
                    'balance': float(balance_val) if balance_val and str(balance_val).replace('.', '').isdigit() else None,
                })
        
        return transactions
