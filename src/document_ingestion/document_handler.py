#!/usr/bin/env python3
"""
Document Handler - File upload, storage, and management
"""

import os
from pathlib import Path
from datetime import datetime
import uuid
import logging
from typing import Optional, Dict, Any
import shutil

logger = logging.getLogger(__name__)

class DocumentHandler:
    """Handles document upload, storage, and retrieval"""
    
    ALLOWED_EXTENSIONS = {'.pdf', '.xlsx', '.xls', '.csv', '.png', '.jpg', '.jpeg'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
    
    def __init__(self, db_operations, data_dir: Path):
        """
        Initialize document handler
        
        Args:
            db_operations: DatabaseOperations instance
            data_dir: Base data directory
        """
        self.db = db_operations
        self.data_dir = data_dir
    
    def upload_document(self, case_id: str, file_path: Path, document_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload and store a document
        
        Args:
            case_id: Case ID
            file_path: Path to file to upload
            document_type: Type of document (optional - will be auto-detected)
        
        Returns:
            Dictionary with document metadata
        """
        # Validate file
        if not self._validate_file(file_path):
            raise ValueError(f"Invalid file: {file_path.name}")
        
        # Generate document ID
        document_id = self._generate_document_id()
        
        # Create case documents folder
        case_docs_dir = self.data_dir / 'cases' / case_id / 'documents'
        case_docs_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy file to case folder
        dest_path = case_docs_dir / file_path.name
        shutil.copy2(file_path, dest_path)
        
        logger.info(f"Uploaded document to {dest_path}")
        
        # Store metadata in database
        doc_metadata = {
            'document_id': document_id,
            'case_id': case_id,
            'file_name': file_path.name,
            'file_type': file_path.suffix.lower(),
            'document_type': document_type or 'Unknown',
            'file_path': str(dest_path),
            'file_size': file_path.stat().st_size,
            'upload_date': datetime.now().isoformat(),
            'extraction_status': 'pending',
            'extraction_confidence': 0.0,
        }
        
        self.db.insert('documents', doc_metadata)
        
        return doc_metadata
    
    def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve document metadata
        
        Args:
            document_id: Document ID
        
        Returns:
            Document metadata or None
        """
        return self.db.select_one('documents', {'document_id': document_id})
    
    def get_case_documents(self, case_id: str) -> list:
        """
        Get all documents for a case
        
        Args:
            case_id: Case ID
        
        Returns:
            List of documents
        """
        return self.db.select('documents', {'case_id': case_id})
    
    def delete_document(self, document_id: str) -> bool:
        """
        Delete a document
        
        Args:
            document_id: Document ID
        
        Returns:
            True if successful
        """
        doc = self.get_document(document_id)
        if not doc:
            return False
        
        # Delete file
        file_path = Path(doc['file_path'])
        if file_path.exists():
            file_path.unlink()
            logger.info(f"Deleted document file: {file_path}")
        
        # Delete from database
        self.db.delete('documents', {'document_id': document_id})
        
        return True
    
    def update_extraction_status(self, document_id: str, status: str, confidence: float = 0.0) -> bool:
        """
        Update extraction status of document
        
        Args:
            document_id: Document ID
            status: Status (pending, extracted, failed)
            confidence: Extraction confidence (0-1)
        
        Returns:
            True if successful
        """
        updates = {
            'extraction_status': status,
            'extraction_confidence': min(1.0, max(0.0, confidence))
        }
        
        rows = self.db.update('documents', updates, {'document_id': document_id})
        return rows > 0
    
    def _validate_file(self, file_path: Path) -> bool:
        """
        Validate file for upload
        
        Args:
            file_path: Path to file
        
        Returns:
            True if valid
        """
        # Check if file exists
        if not file_path.exists():
            logger.error(f"File does not exist: {file_path}")
            return False
        
        # Check file extension
        if file_path.suffix.lower() not in self.ALLOWED_EXTENSIONS:
            logger.error(f"File type not allowed: {file_path.suffix}")
            return False
        
        # Check file size
        file_size = file_path.stat().st_size
        if file_size > self.MAX_FILE_SIZE:
            logger.error(f"File too large: {file_size} bytes")
            return False
        
        # Check file size not zero
        if file_size == 0:
            logger.error(f"File is empty: {file_path}")
            return False
        
        return True
    
    @staticmethod
    def _generate_document_id() -> str:
        """
        Generate unique document ID
        
        Returns:
            Document ID (DOC_UUID)
        """
        return f"DOC_{str(uuid.uuid4())[:8].upper()}"
