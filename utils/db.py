"""
Database utility functions for the application.
"""

import sqlite3
from typing import Any, Dict, List, Optional, Tuple
from contextlib import contextmanager


class DatabaseConnection:
    """Database connection manager."""
    
    def __init__(self, db_path: str = "app.db"):
        """Initialize database connection.
        
        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections.
        
        Yields:
            sqlite3.Connection: Database connection object.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def execute_query(self, query: str, params: Tuple = ()) -> List[Dict[str, Any]]:
        """Execute a SELECT query and return results.
        
        Args:
            query: SQL query string.
            params: Query parameters for safe execution.
            
        Returns:
            List of dictionaries containing query results.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def execute_update(self, query: str, params: Tuple = ()) -> int:
        """Execute an INSERT, UPDATE, or DELETE query.
        
        Args:
            query: SQL query string.
            params: Query parameters for safe execution.
            
        Returns:
            Number of rows affected.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            return cursor.rowcount
    
    def execute_many(self, query: str, params_list: List[Tuple]) -> int:
        """Execute multiple INSERT, UPDATE, or DELETE queries.
        
        Args:
            query: SQL query string.
            params_list: List of parameter tuples.
            
        Returns:
            Total number of rows affected.
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, params_list)
            return cursor.rowcount
    
    def create_table(self, table_name: str, schema: str) -> None:
        """Create a table if it doesn't exist.
        
        Args:
            table_name: Name of the table to create.
            schema: SQL schema definition for the table.
        """
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
    
    def drop_table(self, table_name: str) -> None:
        """Drop a table if it exists.
        
        Args:
            table_name: Name of the table to drop.
        """
        query = f"DROP TABLE IF EXISTS {table_name}"
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)


# Default database instance
db = DatabaseConnection()


def init_db(db_path: str = "app.db") -> DatabaseConnection:
    """Initialize the database with default tables.
    
    Args:
        db_path: Path to the SQLite database file.
        
    Returns:
        DatabaseConnection instance.
    """
    database = DatabaseConnection(db_path)
    
    # Example tables - customize as needed
    database.create_table(
        "users",
        """
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        """
    )
    
    return database


def get_db() -> DatabaseConnection:
    """Get the default database instance.
    
    Returns:
        DatabaseConnection instance.
    """
    return db
