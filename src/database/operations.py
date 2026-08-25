#!/usr/bin/env python3
"""
Database CRUD Operations
"""

import sqlite3
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class DatabaseOperations:
    """Database CRUD operations"""
    
    def __init__(self, connection):
        self.conn = connection
    
    def insert(self, table: str, data: Dict[str, Any]) -> str:
        """Insert a record into a table"""
        try:
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            values = tuple(data.values())
            query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
            cursor = self.conn.execute(query, values)
            self.conn.commit()
            logger.info(f"Inserted record into {table}")
            return str(cursor.lastrowid)
        except sqlite3.Error as e:
            logger.error(f"Insert error in {table}: {e}")
            self.conn.rollback()
            raise
    
    def select(self, table: str, where: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Select records from a table"""
        try:
            if where:
                conditions = ' AND '.join([f"{k} = ?" for k in where.keys()])
                values = tuple(where.values())
                query = f"SELECT * FROM {table} WHERE {conditions}"
                cursor = self.conn.execute(query, values)
            else:
                query = f"SELECT * FROM {table}"
                cursor = self.conn.execute(query)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            logger.error(f"Select error from {table}: {e}")
            raise
    
    def select_one(self, table: str, where: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Select a single record from a table"""
        results = self.select(table, where)
        return results[0] if results else None
    
    def update(self, table: str, data: Dict[str, Any], where: Dict[str, Any]) -> int:
        """Update records in a table"""
        try:
            set_clause = ', '.join([f"{k} = ?" for k in data.keys()])
            where_clause = ' AND '.join([f"{k} = ?" for k in where.keys()])
            values = tuple(data.values()) + tuple(where.values())
            query = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
            cursor = self.conn.execute(query, values)
            self.conn.commit()
            logger.info(f"Updated {cursor.rowcount} records in {table}")
            return cursor.rowcount
        except sqlite3.Error as e:
            logger.error(f"Update error in {table}: {e}")
            self.conn.rollback()
            raise
    
    def delete(self, table: str, where: Dict[str, Any]) -> int:
        """Delete records from a table"""
        try:
            where_clause = ' AND '.join([f"{k} = ?" for k in where.keys()])
            values = tuple(where.values())
            query = f"DELETE FROM {table} WHERE {where_clause}"
            cursor = self.conn.execute(query, values)
            self.conn.commit()
            logger.info(f"Deleted {cursor.rowcount} records from {table}")
            return cursor.rowcount
        except sqlite3.Error as e:
            logger.error(f"Delete error from {table}: {e}")
            self.conn.rollback()
            raise
