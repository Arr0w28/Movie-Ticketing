# utils/database.py
import psycopg2
import psycopg2.extras
import streamlit as st
from typing import Optional, Dict

class DatabaseConnection:
    def __init__(self):
        """Initialize database connection handler"""
        self.connection = None
        
    def connect(self) -> psycopg2.extensions.connection:
        """Establish database connection using Streamlit secrets"""
        try:
            if self.connection is None or self.connection.closed:
                self.connection = psycopg2.connect(
                    dbname=st.secrets["postgres"]["database"],
                    user=st.secrets["postgres"]["user"],
                    password=st.secrets["postgres"]["password"],
                    host=st.secrets["postgres"]["host"],
                    port=st.secrets["postgres"]["port"]
                )
                # Set autocommit to False for transaction control
                self.connection.autocommit = False
            return self.connection
        except Exception as e:
            st.error(f"Database connection error: {str(e)}")
            raise

    def close(self):
        """Close database connection"""
        if self.connection and not self.connection.closed:
            self.connection.close()

def get_db_connection() -> psycopg2.extensions.connection:
    """Get database connection (convenience function)"""
    db = DatabaseConnection()
    return db.connect()

def execute_query(query: str, params: Optional[tuple] = None, fetch: bool = True) -> Optional[Dict]:
    """
    Execute a database query with proper connection handling
    
    Args:
        query (str): SQL query to execute
        params (tuple, optional): Query parameters
        fetch (bool): Whether to fetch results (True for SELECT queries)
        
    Returns:
        Optional[Dict]: Query results if fetch is True, None otherwise
    """
    conn = None
    try:
        conn = get_db_connection()
        # Use RealDictCursor to get dictionary-like results
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
            cursor.execute(query, params)
            if fetch:
                result = cursor.fetchall()
                return result
            conn.commit()
            return None
    except Exception as e:
        st.error(f"Database error: {str(e)}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()