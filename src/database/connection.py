#!/usr/bin/env python3
"""
Database Connection Manager - SQLite
"""

import sqlite3
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """SQLite database connection manager"""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.connection: Optional[sqlite3.Connection] = None
    
    def connect(self) -> sqlite3.Connection:
        """Establish database connection"""
        if self.connection is None:
            try:
                self.connection = sqlite3.connect(str(self.db_path))
                self.connection.row_factory = sqlite3.Row
                self.connection.execute("PRAGMA foreign_keys = ON")
                logger.info(f"Connected to database: {self.db_path}")
            except sqlite3.Error as e:
                logger.error(f"Database connection error: {e}")
                raise
        return self.connection
    
    def disconnect(self) -> None:
        """Close database connection"""
        if self.connection:
            self.connection.close()
            self.connection = None
            logger.info(f"Disconnected from database")
    
    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute a query"""
        try:
            cursor = self.connect().execute(query, params)
            return cursor
        except sqlite3.Error as e:
            logger.error(f"Query execution error: {e}")
            raise
    
    def commit(self) -> None:
        """Commit transaction"""
        if self.connection:
            self.connection.commit()
    
    def rollback(self) -> None:
        """Rollback transaction"""
        if self.connection:
            self.connection.rollback()
    
    def create_tables(self) -> None:
        """Create database schema if tables don't exist"""
        from .models import SCHEMA
        try:
            for table_name, create_statement in SCHEMA.items():
                self.execute(create_statement)
            self.commit()
            logger.info("Database schema initialized")
        except sqlite3.Error as e:
            logger.error(f"Error creating tables: {e}")
            self.rollback()
            raise
