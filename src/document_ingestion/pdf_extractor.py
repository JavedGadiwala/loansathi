#!/usr/bin/env python3
"""
PDF Extractor - Extract data from PDF bank statements
"""

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime
import re

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

logger = logging.getLogger(__name__)

class PDFExtractor:
    """Extract data from PDF documents"""
    
    def __init__(self):
        """
        Initialize PDF extractor
        """
        if pdfplumber is None:
            logger.warning("pdfplumber not installed. PDF extraction will not work.")
    
    def extract_text(self, pdf_path: Path) -> str:
        """
        Extract all text from PDF
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            Extracted text
        """
        if pdfplumber is None:
            logger.error("pdfplumber not installed")
            return ""
        
        try:
            text = ""
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
                    text += "\n"
            
            logger.info(f"Extracted text from {pdf_path.name} ({len(text)} chars)")
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            return ""
    
    def extract_tables(self, pdf_path: Path) -> List[List[Dict]]:
        """
        Extract tables from PDF
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            List of tables (each table is list of dictionaries)
        """
        if pdfplumber is None:
            logger.error("pdfplumber not installed")
            return []
        
        try:
            tables = []
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_tables = page.extract_tables()
                    if page_tables:
                        for table in page_tables:
                            # Convert to list of dicts
                            if table:
                                headers = table[0]
                                rows = [
                                    dict(zip(headers, row))
                                    for row in table[1:]
                                ]
                                tables.append(rows)
            
            logger.info(f"Extracted {len(tables)} tables from {pdf_path.name}")
            return tables
        except Exception as e:
            logger.error(f"Error extracting tables from PDF: {e}")
            return []
    
    def extract_metadata(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Extract metadata from PDF
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            PDF metadata
        """
        if pdfplumber is None:
            return {}
        
        try:
            metadata = {}
            with pdfplumber.open(pdf_path) as pdf:
                metadata['num_pages'] = len(pdf.pages)
                metadata['metadata'] = pdf.metadata if pdf.metadata else {}
            
            return metadata
        except Exception as e:
            logger.error(f"Error extracting metadata: {e}")
            return {}
    
    def extract_bank_statement_data(self, pdf_path: Path) -> Dict[str, Any]:
        """
        Extract bank statement data from PDF
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            Dictionary with extracted bank statement data
        """
        result = {
            'success': False,
            'bank_name': None,
            'account_number': None,
            'statement_period': None,
            'transactions': [],
            'confidence': 0.0,
            'raw_text': "",
            'tables': [],
            'errors': []
        }
        
        try:
            # Extract text
            text = self.extract_text(pdf_path)
            result['raw_text'] = text
            
            # Extract tables
            tables = self.extract_tables(pdf_path)
            result['tables'] = tables
            
            # Try to detect bank name
            bank_name = self._detect_bank(text)
            result['bank_name'] = bank_name
            
            # Try to extract account number
            account = self._extract_account_number(text)
            result['account_number'] = account
            
            # Try to extract statement period
            period = self._extract_statement_period(text)
            result['statement_period'] = period
            
            # Mark as partially successful
            result['success'] = True
            result['confidence'] = 0.7  # Will be refined in Phase 2.5
            
            logger.info(f"Extracted bank statement data from {pdf_path.name}")
            return result
        
        except Exception as e:
            logger.error(f"Error extracting bank statement: {e}")
            result['errors'].append(str(e))
            return result
    
    @staticmethod
    def _detect_bank(text: str) -> Optional[str]:
        """
        Detect bank name from text
        
        Args:
            text: Extracted text
        
        Returns:
            Bank name or None
        """
        banks = {
            'HDFC': r'hdfc bank|hdfc',
            'ICICI': r'icici bank|icici',
            'SBI': r'state bank|sbi',
            'Axis': r'axis bank|axis',
            'Kotak': r'kotak bank|kotak',
            'IDBI': r'idbi bank|idbi',
            'Canara': r'canara bank|canara',
            'BOB': r'bank of baroda|bob',
        }
        
        text_lower = text.lower()
        for bank, pattern in banks.items():
            if re.search(pattern, text_lower):
                return bank
        
        return None
    
    @staticmethod
    def _extract_account_number(text: str) -> Optional[str]:
        """
        Extract account number from text
        
        Args:
            text: Extracted text
        
        Returns:
            Account number or None
        """
        # Common patterns: 10-18 digits
        pattern = r'(?:Account|A/C|Acct)[#\s]*[:=]?\s*([0-9]{10,18})'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            return match.group(1)
        
        # Try general pattern
        pattern = r'\b[0-9]{10,18}\b'
        matches = re.findall(pattern, text)
        
        if matches:
            return matches[0]
        
        return None
    
    @staticmethod
    def _extract_statement_period(text: str) -> Optional[Dict[str, str]]:
        """
        Extract statement period from text
        
        Args:
            text: Extracted text
        
        Returns:
            Dictionary with start_date and end_date, or None
        """
        # Look for period patterns
        pattern = r'(?:Period|Statement Period|From|For)[\s]*(?:[:|])?\s*([\d\-\/]+)\s*(?:to|TO|-|and)\s*([\d\-\/]+)'
        match = re.search(pattern, text, re.IGNORECASE)
        
        if match:
            try:
                start_date = match.group(1)
                end_date = match.group(2)
                return {
                    'start_date': start_date,
                    'end_date': end_date
                }
            except:
                pass
        
        return None
