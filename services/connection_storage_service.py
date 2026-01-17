"""
SQLite service for storing and managing Cosmos DB connections
"""
import sqlite3
import json
from typing import List, Optional, Tuple
from pathlib import Path
from models.connection_config import ConnectionConfig


class ConnectionStorageService:
    """Service for managing stored connections in SQLite"""
    
    def __init__(self, db_path: str = "connections.db"):
        """Initialize the storage service with a database path"""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database and create tables if they don't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                cosmos_endpoint TEXT NOT NULL,
                service_url TEXT NOT NULL,
                client_id TEXT NOT NULL,
                client_secret TEXT NOT NULL,
                resource TEXT NOT NULL,
                grant_type TEXT DEFAULT 'client_credentials',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def save_connection(self, name: str, config: ConnectionConfig) -> Tuple[bool, str]:
        """
        Save a connection configuration
        
        Args:
            name: Name for the connection
            config: Connection configuration
            
        Returns:
            Tuple of (success, message)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO connections (name, cosmos_endpoint, service_url, client_id, 
                                       client_secret, resource, grant_type)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                name,
                config.cosmos_endpoint,
                config.service_url,
                config.client_id,
                config.client_secret,
                config.resource,
                config.grant_type
            ))
            
            conn.commit()
            conn.close()
            
            return True, "Connection saved successfully"
        except sqlite3.IntegrityError:
            return False, f"Connection with name '{name}' already exists"
        except Exception as e:
            return False, f"Error saving connection: {str(e)}"
    
    def get_all_connections(self) -> List[Tuple[int, str]]:
        """
        Get all saved connections (id and name only)
        
        Returns:
            List of tuples (id, name)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, name FROM connections ORDER BY name")
            results = cursor.fetchall()
            
            conn.close()
            return results
        except Exception as e:
            print(f"Error getting connections: {e}")
            return []
    
    def get_connection(self, connection_id: int) -> Optional[Tuple[str, ConnectionConfig]]:
        """
        Get a specific connection by ID
        
        Args:
            connection_id: The connection ID
            
        Returns:
            Tuple of (name, ConnectionConfig) or None if not found
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT name, cosmos_endpoint, service_url, client_id, client_secret, 
                       resource, grant_type
                FROM connections 
                WHERE id = ?
            """, (connection_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                name = result[0]
                config = ConnectionConfig(
                    cosmos_endpoint=result[1],
                    service_url=result[2],
                    client_id=result[3],
                    client_secret=result[4],
                    resource=result[5],
                    grant_type=result[6]
                )
                return name, config
            return None
        except Exception as e:
            print(f"Error getting connection: {e}")
            return None
    
    def delete_connection(self, connection_id: int) -> Tuple[bool, str]:
        """
        Delete a connection by ID
        
        Args:
            connection_id: The connection ID to delete
            
        Returns:
            Tuple of (success, message)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM connections WHERE id = ?", (connection_id,))
            
            if cursor.rowcount > 0:
                conn.commit()
                conn.close()
                return True, "Connection deleted successfully"
            else:
                conn.close()
                return False, "Connection not found"
        except Exception as e:
            return False, f"Error deleting connection: {str(e)}"
    
    def update_connection(self, connection_id: int, name: str, config: ConnectionConfig) -> Tuple[bool, str]:
        """
        Update an existing connection
        
        Args:
            connection_id: The connection ID to update
            name: New name for the connection
            config: New connection configuration
            
        Returns:
            Tuple of (success, message)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE connections 
                SET name = ?, cosmos_endpoint = ?, service_url = ?, client_id = ?,
                    client_secret = ?, resource = ?, grant_type = ?
                WHERE id = ?
            """, (
                name,
                config.cosmos_endpoint,
                config.service_url,
                config.client_id,
                config.client_secret,
                config.resource,
                config.grant_type,
                connection_id
            ))
            
            if cursor.rowcount > 0:
                conn.commit()
                conn.close()
                return True, "Connection updated successfully"
            else:
                conn.close()
                return False, "Connection not found"
        except sqlite3.IntegrityError:
            return False, f"Connection with name '{name}' already exists"
        except Exception as e:
            return False, f"Error updating connection: {str(e)}"
