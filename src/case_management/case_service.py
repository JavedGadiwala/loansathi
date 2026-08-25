#!/usr/bin/env python3
"""
Case Management Service
Handles case creation, retrieval, update, and listing
"""

from datetime import datetime
from typing import List, Dict, Optional, Any
import uuid
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class CaseService:
    """Service for managing loan cases"""
    
    def __init__(self, db_operations, data_dir: Path):
        """
        Initialize case service
        
        Args:
            db_operations: DatabaseOperations instance
            data_dir: Base data directory
        """
        self.db = db_operations
        self.data_dir = data_dir
    
    def create_case(self, client_data: Dict[str, Any]) -> str:
        """
        Create a new case
        
        Args:
            client_data: Dictionary with case information
        
        Returns:
            Generated case_id
        """
        case_id = self._generate_case_id()
        
        case_data = {
            'case_id': case_id,
            'client_name': client_data.get('client_name', ''),
            'pan_identifier': client_data.get('pan_identifier', None),
            'business_name': client_data.get('business_name', None),
            'constitution': client_data.get('constitution', 'Individual'),
            'industry': client_data.get('industry', None),
            'location': client_data.get('location', None),
            'existing_banker': client_data.get('existing_banker', None),
            'loan_purpose': client_data.get('loan_purpose', ''),
            'requested_amount': float(client_data.get('requested_amount', 0)),
            'requested_tenure_months': int(client_data.get('requested_tenure_months', 0)),
            'expected_interest_rate': float(client_data.get('expected_interest_rate', 0)),
            'assessment_date': client_data.get('assessment_date', datetime.now().strftime('%Y-%m-%d')),
            'notes': client_data.get('notes', ''),
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        # Create case in database
        self.db.insert('cases', case_data)
        
        # Create case folder structure
        case_folder = self.data_dir / 'cases' / case_id
        case_folder.mkdir(parents=True, exist_ok=True)
        (case_folder / 'documents').mkdir(exist_ok=True)
        (case_folder / 'extractions').mkdir(exist_ok=True)
        (case_folder / 'reports').mkdir(exist_ok=True)
        
        logger.info(f"Created case: {case_id}")
        return case_id
    
    def get_case(self, case_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a case by ID
        
        Args:
            case_id: Case ID
        
        Returns:
            Case data or None if not found
        """
        return self.db.select_one('cases', {'case_id': case_id})
    
    def list_cases(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List all cases, optionally filtered by status
        
        Args:
            status: Optional status filter
        
        Returns:
            List of cases
        """
        if status:
            return self.db.select('cases', {'status': status})
        return self.db.select('cases')
    
    def update_case(self, case_id: str, updates: Dict[str, Any]) -> bool:
        """
        Update a case
        
        Args:
            case_id: Case ID
            updates: Dictionary of fields to update
        
        Returns:
            True if update successful
        """
        updates['updated_at'] = datetime.now().isoformat()
        rows_updated = self.db.update('cases', updates, {'case_id': case_id})
        
        if rows_updated > 0:
            logger.info(f"Updated case: {case_id}")
            return True
        return False
    
    def close_case(self, case_id: str) -> bool:
        """
        Close a case (mark as inactive)
        
        Args:
            case_id: Case ID
        
        Returns:
            True if successful
        """
        return self.update_case(case_id, {'status': 'inactive'})
    
    def delete_case(self, case_id: str) -> bool:
        """
        Permanently delete a case
        
        Args:
            case_id: Case ID
        
        Returns:
            True if successful
        """
        # Delete from database (cascade will delete related records)
        rows_deleted = self.db.delete('cases', {'case_id': case_id})
        
        # Delete case folder
        case_folder = self.data_dir / 'cases' / case_id
        if case_folder.exists():
            import shutil
            shutil.rmtree(case_folder)
            logger.info(f"Deleted case folder: {case_folder}")
        
        logger.info(f"Deleted case: {case_id}")
        return rows_deleted > 0
    
    def get_case_folder(self, case_id: str) -> Path:
        """
        Get the folder path for a case
        
        Args:
            case_id: Case ID
        
        Returns:
            Path to case folder
        """
        return self.data_dir / 'cases' / case_id
    
    def duplicate_case(self, case_id: str) -> str:
        """
        Create a duplicate of an existing case
        
        Args:
            case_id: Case ID to duplicate
        
        Returns:
            New case_id
        """
        original_case = self.get_case(case_id)
        if not original_case:
            raise ValueError(f"Case {case_id} not found")
        
        # Create new case with same data
        new_case_data = dict(original_case)
        del new_case_data['case_id']
        
        return self.create_case(new_case_data)
    
    @staticmethod
    def _generate_case_id() -> str:
        """
        Generate a unique case ID
        
        Returns:
            Case ID (CASE_YYYYMMDD_UUID)
        """
        date_part = datetime.now().strftime('%Y%m%d')
        uuid_part = str(uuid.uuid4())[:8].upper()
        return f"CASE_{date_part}_{uuid_part}"
