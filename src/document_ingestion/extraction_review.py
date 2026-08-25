#!/usr/bin/env python3
"""
Extraction Review System - Preview and verify extracted data
"""

import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

class ExtractionReview:
    """Manage extraction review and verification"""
    
    def __init__(self, db_operations):
        """
        Initialize extraction review system
        
        Args:
            db_operations: DatabaseOperations instance
        """
        self.db = db_operations
    
    def create_extraction_session(self, case_id: str, document_id: str, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an extraction session for review
        
        Args:
            case_id: Case ID
            document_id: Document ID
            extracted_data: Extracted data from document
        
        Returns:
            Session metadata
        """
        session_id = f"EXT_{str(uuid.uuid4())[:8].upper()}"
        
        session = {
            'session_id': session_id,
            'case_id': case_id,
            'document_id': document_id,
            'total_transactions': len(extracted_data.get('transactions', [])),
            'reviewed_transactions': 0,
            'approved_transactions': 0,
            'rejected_transactions': 0,
            'status': 'in_progress',
            'created_at': datetime.now().isoformat(),
            'completed_at': None,
        }
        
        logger.info(f"Created extraction session: {session_id}")
        return session
    
    def get_transactions_for_review(self, extracted_data: Dict[str, Any], page: int = 1, per_page: int = 10) -> Dict[str, Any]:
        """
        Get paginated list of transactions for review
        
        Args:
            extracted_data: Extracted data
            page: Page number
            per_page: Records per page
        
        Returns:
            Paginated transactions with metadata
        """
        transactions = extracted_data.get('transactions', [])
        total = len(transactions)
        start = (page - 1) * per_page
        end = start + per_page
        
        page_transactions = transactions[start:end]
        
        return {
            'page': page,
            'per_page': per_page,
            'total': total,
            'total_pages': (total + per_page - 1) // per_page,
            'transactions': page_transactions,
            'has_next': end < total,
            'has_prev': page > 1,
        }
    
    def verify_transaction(self, transaction: Dict[str, Any], corrections: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Verify and optionally correct a transaction
        
        Args:
            transaction: Transaction to verify
            corrections: Optional corrections to apply
        
        Returns:
            Verified transaction
        """
        verified = dict(transaction)
        
        # Apply corrections if provided
        if corrections:
            for key, value in corrections.items():
                if key in verified and value is not None:
                    verified[key] = value
                    logger.debug(f"Corrected transaction field: {key}")
        
        # Mark as verified
        verified['review_status'] = 'verified'
        verified['verified_at'] = datetime.now().isoformat()
        
        return verified
    
    def bulk_update_transactions(self, transactions: List[Dict[str, Any]], updates: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Apply bulk updates to multiple transactions
        
        Args:
            transactions: List of transactions
            updates: Updates to apply to all
        
        Returns:
            Updated transactions
        """
        updated = []
        
        for tx in transactions:
            updated_tx = dict(tx)
            updated_tx.update(updates)
            updated_tx['review_status'] = 'bulk_updated'
            updated.append(updated_tx)
        
        logger.info(f"Bulk updated {len(updated)} transactions")
        return updated
    
    def validate_extraction(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate extracted data quality
        
        Args:
            extracted_data: Extracted data
        
        Returns:
            Validation report
        """
        transactions = extracted_data.get('transactions', [])
        
        report = {
            'total_transactions': len(transactions),
            'transactions_with_dates': 0,
            'transactions_with_amounts': 0,
            'transactions_with_narration': 0,
            'transactions_with_balance': 0,
            'avg_confidence': 0.0,
            'issues': [],
            'quality_score': 0.0,
        }
        
        if not transactions:
            report['issues'].append('No transactions extracted')
            return report
        
        total_confidence = 0.0
        
        for tx in transactions:
            if tx.get('date'):
                report['transactions_with_dates'] += 1
            if tx.get('debit', 0) > 0 or tx.get('credit', 0) > 0:
                report['transactions_with_amounts'] += 1
            if tx.get('narration'):
                report['transactions_with_narration'] += 1
            if tx.get('balance') is not None:
                report['transactions_with_balance'] += 1
            
            total_confidence += tx.get('confidence', 0.0)
        
        report['avg_confidence'] = total_confidence / len(transactions) if transactions else 0.0
        
        # Calculate quality score
        date_score = report['transactions_with_dates'] / len(transactions)
        amount_score = report['transactions_with_amounts'] / len(transactions)
        narration_score = report['transactions_with_narration'] / len(transactions)
        
        report['quality_score'] = (date_score * 0.4 + amount_score * 0.35 + narration_score * 0.25)
        
        # Add issues if quality is low
        if report['quality_score'] < 0.6:
            report['issues'].append(f"Low quality extraction (score: {report['quality_score']:.2f})")
        if report['avg_confidence'] < 0.6:
            report['issues'].append(f"Low extraction confidence (avg: {report['avg_confidence']:.2f})")
        if report['transactions_with_dates'] < len(transactions) * 0.8:
            report['issues'].append(f"Some transactions missing dates ({report['transactions_with_dates']}/{len(transactions)})")
        if report['transactions_with_amounts'] < len(transactions) * 0.8:
            report['issues'].append(f"Some transactions missing amounts ({report['transactions_with_amounts']}/{len(transactions)})")
        
        logger.info(f"Validation report - Quality score: {report['quality_score']:.2f}, Issues: {len(report['issues'])}")
        
        return report
    
    def get_extraction_summary(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get summary of extracted data
        
        Args:
            extracted_data: Extracted data
        
        Returns:
            Summary report
        """
        transactions = extracted_data.get('transactions', [])
        
        # Calculate totals
        total_debit = sum(tx.get('debit', 0) for tx in transactions)
        total_credit = sum(tx.get('credit', 0) for tx in transactions)
        
        # Get date range
        dates = [tx.get('date') for tx in transactions if tx.get('date')]
        min_date = min(dates) if dates else None
        max_date = max(dates) if dates else None
        
        # Get categories
        categories = {}
        for tx in transactions:
            cat = tx.get('category', 'Other')
            categories[cat] = categories.get(cat, 0) + 1
        
        return {
            'bank_name': extracted_data.get('bank_name'),
            'account_number': extracted_data.get('account_number'),
            'statement_period': extracted_data.get('statement_period'),
            'total_transactions': len(transactions),
            'total_debit': total_debit,
            'total_credit': total_credit,
            'net_amount': total_credit - total_debit,
            'date_range': {
                'start': min_date,
                'end': max_date,
            },
            'categories': categories,
            'confidence': extracted_data.get('confidence', 0.0),
        }
