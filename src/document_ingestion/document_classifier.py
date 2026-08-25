#!/usr/bin/env python3
"""
Document Classifier - Detect document type and bank
"""

import logging
from pathlib import Path
from typing import Dict, Any, Optional
import re

logger = logging.getLogger(__name__)

class DocumentClassifier:
    """Classify documents by type and bank"""
    
    # Bank patterns
    BANK_PATTERNS = {
        'HDFC': r'hdfc bank|hdfc|hdfc\s+bank',
        'ICICI': r'icici bank|icici|icici\s+bank',
        'SBI': r'state bank of india|state bank|sbi',
        'Axis': r'axis bank|axis',
        'Kotak': r'kotak bank|kotak',
        'IDBI': r'idbi bank|idbi',
        'Canara': r'canara bank|canara',
        'BOB': r'bank of baroda|bob',
        'IndusInd': r'indusind bank|indusind',
        'Yes Bank': r'yes bank|yes',
        'RBL': r'rbl bank|rbl',
        'Federal': r'federal bank|federal',
    }
    
    # Document type patterns
    DOCTYPE_PATTERNS = {
        'Bank Statement': r'statement|bank|account|monthly|transactions',
        'ITR': r'itr|income tax return|form 16|tax return',
        'GST': r'gst|goods and services tax|inward|outward|invoice',
        'Financial': r'financial|balance sheet|p&l|profit|loss|income|expense',
        'Invoices': r'invoice|bill|purchase|sales|credit note|debit note',
        'Other': r'document|report|statement'
    }
    
    def __init__(self):
        """Initialize document classifier"""
        pass
    
    def classify_document(self, file_name: str, file_content: Optional[str] = None) -> Dict[str, Any]:
        """
        Classify a document by type and bank
        
        Args:
            file_name: Name of the document file
            file_content: Optional file content (text) for better classification
        
        Returns:
            Dictionary with classification results
        """
        result = {
            'document_type': 'Unknown',
            'bank_name': None,
            'confidence': 0.0,
            'filename_match': None,
            'content_match': None
        }
        
        # Classify by filename
        filename_lower = file_name.lower()
        
        # Try to detect bank
        for bank, pattern in self.BANK_PATTERNS.items():
            if re.search(pattern, filename_lower, re.IGNORECASE):
                result['bank_name'] = bank
                result['filename_match'] = 'bank'
                result['confidence'] += 0.3
                break
        
        # Try to detect document type
        for doc_type, pattern in self.DOCTYPE_PATTERNS.items():
            if re.search(pattern, filename_lower, re.IGNORECASE):
                result['document_type'] = doc_type
                result['filename_match'] = 'type'
                result['confidence'] += 0.4
                break
        
        # Refine with file content if provided
        if file_content:
            result = self._classify_by_content(file_content, result)
        
        # Cap confidence at 1.0
        result['confidence'] = min(1.0, result['confidence'])
        
        logger.info(f"Classified '{file_name}' as {result['document_type']} (bank: {result['bank_name']}, confidence: {result['confidence']:.2f})")
        
        return result
    
    def _classify_by_content(self, content: str, existing_result: Dict) -> Dict:
        """
        Refine classification using file content
        
        Args:
            content: File content (text)
            existing_result: Existing classification result
        
        Returns:
            Updated classification result
        """
        content_lower = content.lower()[:2000]  # Use first 2000 chars
        
        # Try to detect bank from content
        if not existing_result['bank_name']:
            for bank, pattern in self.BANK_PATTERNS.items():
                if re.search(pattern, content_lower, re.IGNORECASE):
                    existing_result['bank_name'] = bank
                    existing_result['content_match'] = 'bank'
                    existing_result['confidence'] += 0.2
                    break
        
        # Try to detect document type from content
        if existing_result['document_type'] == 'Unknown':
            for doc_type, pattern in self.DOCTYPE_PATTERNS.items():
                if re.search(pattern, content_lower, re.IGNORECASE):
                    existing_result['document_type'] = doc_type
                    existing_result['content_match'] = 'type'
                    existing_result['confidence'] += 0.3
                    break
        
        return existing_result
    
    def classify_multiple(self, file_names: list, file_contents: Optional[list] = None) -> list:
        """
        Classify multiple documents
        
        Args:
            file_names: List of file names
            file_contents: Optional list of file contents
        
        Returns:
            List of classification results
        """
        results = []
        
        for i, file_name in enumerate(file_names):
            content = file_contents[i] if file_contents and i < len(file_contents) else None
            result = self.classify_document(file_name, content)
            results.append(result)
        
        return results
