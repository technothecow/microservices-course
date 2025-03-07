import psycopg2
from psycopg2 import pool
from psycopg2 import extras
from typing import Dict, List, Any, Optional, Union, Tuple
import os
import logging

class PostgresDB:
    """
    A singleton class for PostgreSQL database operations.
    Provides connection pooling and methods for common database operations.
    """
    _instance = None
    _connection_pool = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PostgresDB, cls).__new__(cls)
            cls._setup_connection_pool()
        return cls._instance
    
    @classmethod
    def _setup_connection_pool(cls):
        """Set up the connection pool using environment variables."""
        try:
            # Get database connection parameters from environment variables
            host = os.environ.get("DB_HOST", "localhost")
            port = os.environ.get("DB_PORT", "5432")
            database = os.environ.get("DB_NAME", "postgres")
            user = os.environ.get("DB_USER", "postgres")
            password = os.environ.get("DB_PASSWORD", "")
            
            # Create a connection pool
            cls._connection_pool = pool.SimpleConnectionPool(
                1, 10,  # min, max connections
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
            )
            
            logging.info("PostgreSQL connection pool created successfully")
        except Exception as e:
            logging.error(f"Error creating connection pool: {e}")
            raise

    def get_connection(self):
        """Get a connection from the pool."""
        if self._connection_pool:
            return self._connection_pool.getconn()
        else:
            raise Exception("Connection pool not initialized")
    
    def release_connection(self, conn):
        """Return a connection to the pool."""
        if self._connection_pool:
            self._connection_pool.putconn(conn)
    
    def query(self, query_string, params=None) -> List[Dict[str, Any]]:
        """Execute a query and return results as a list of dictionaries."""
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cursor:
                cursor.execute(query_string, params)
                
                if cursor.description:
                    return list(cursor.fetchall())
                return []
        except Exception as e:
            logging.error(f"Error executing query: {e}")
            raise
        finally:
            if conn:
                self.release_connection(conn)
    
    def execute(self, query_string, params=None) -> int:
        """Execute a non-query SQL command."""
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query_string, params)
                conn.commit()
                return cursor.rowcount
        except Exception as e:
            if conn:
                conn.rollback()
            logging.error(f"Error executing command: {e}")
            raise
        finally:
            if conn:
                self.release_connection(conn)
    
    def insert(self, table: str, data: Dict[str, Any]) -> Optional[int]:
        """Insert a row into a table."""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING id"
        
        conn = None
        try:
            conn = self.get_connection()
            with conn.cursor() as cursor:
                cursor.execute(query, list(data.values()))
                conn.commit()
                result = cursor.fetchone()
                return result[0] if result else None
        except Exception as e:
            if conn:
                conn.rollback()
            logging.error(f"Error inserting data: {e}")
            raise
        finally:
            if conn:
                self.release_connection(conn)
    
    def update(self, table: str, data: Dict[str, Any], condition: str, condition_params: tuple) -> int:
        """Update rows in a table."""
        set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
        query = f"UPDATE {table} SET {set_clause} WHERE {condition}"
        
        params = list(data.values()) + list(condition_params)
        return self.execute(query, params)
    
    def delete(self, table: str, condition: str, condition_params: tuple) -> int:
        """Delete rows from a table."""
        query = f"DELETE FROM {table} WHERE {condition}"
        return self.execute(query, condition_params)
    
    def transaction(self):
        """Get a connection for a transaction (context manager)."""
        class Transaction:
            def __init__(self, db):
                self.db = db
                self.conn = None
            
            def __enter__(self):
                self.conn = self.db.get_connection()
                return self.conn
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                if exc_type is None:
                    self.conn.commit()
                else:
                    self.conn.rollback()
                self.db.release_connection(self.conn)
        
        return Transaction(self)
    
    def close_all_connections(self):
        """Close all connections in the pool."""
        if self._connection_pool:
            self._connection_pool.closeall()
            logging.info("All database connections closed")