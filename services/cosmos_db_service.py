"""
Service layer for Azure Cosmos DB operations
"""
from typing import List, Dict, Any, Optional
import requests
import certifi
from azure.cosmos import CosmosClient, exceptions
from models.connection_config import ConnectionConfig


class CosmosDBService:
    """Service for interacting with Azure Cosmos DB"""
    
    def __init__(self):
        self.client: Optional[CosmosClient] = None
        self.config: Optional[ConnectionConfig] = None
        self.connected = False
        self.access_token: Optional[str] = None
    
    def _get_access_token(self, config: ConnectionConfig) -> tuple[bool, str, Optional[str]]:
        """
        Get OAuth2 access token from Azure AD
        
        Returns:
            tuple: (success: bool, message: str, token: Optional[str])
        """
        try:
            # Prepare OAuth2 token request
            token_url = f"{config.service_url}/oauth2/token"
            
            payload = {
                'grant_type': config.grant_type,
                'client_id': config.client_id,
                'client_secret': config.client_secret,
                'resource': config.resource
            }
            
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            
            # Request token with certifi for certificate validation (Zscaler support)
            response = requests.post(token_url, data=payload, headers=headers, verify=certifi.where())
            
            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get('access_token')
                if access_token:
                    return True, "Token acquired successfully", access_token
                else:
                    return False, "No access token in response", None
            else:
                error_msg = response.text
                return False, f"Token request failed: {error_msg}", None
        
        except Exception as e:
            return False, f"Error acquiring token: {str(e)}", None
    
    def connect(self, config: ConnectionConfig) -> tuple[bool, str]:
        """
        Connect to Azure Cosmos DB using OAuth2 authentication
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            if not config.is_valid():
                return False, "Invalid connection configuration"
            
            # Get OAuth2 access token
            success, message, token = self._get_access_token(config)
            if not success or not token:
                return False, message
            
            self.access_token = token
            
            # Create Cosmos client with token
            # Note: Using credential as a simple dict with the token
            credential = {'access_token': token}
            
            # For OAuth2, we need to use a different approach
            # Azure Cosmos SDK expects resource tokens or master keys
            # We'll use the token as credential in a custom way
            try:
                # Try creating client with token-based auth
                from azure.core.credentials import AccessToken
                from datetime import datetime, timedelta
                
                class TokenCredential:
                    def __init__(self, token):
                        self.token = token
                    
                    def get_token(self, *scopes, **kwargs):
                        # Return token with expiry (default 1 hour)
                        return AccessToken(self.token, int((datetime.now() + timedelta(hours=1)).timestamp()))
                
                token_credential = TokenCredential(token)
                # Use certifi for certificate validation (Zscaler support)
                connection_verify = certifi.where()
                self.client = CosmosClient(
                    config.cosmos_endpoint,
                    credential=token_credential,
                    connection_verify=connection_verify
                )
                
            except Exception as e:
                return False, f"Failed to create Cosmos client: {str(e)}"
            
            self.config = config
            
            # Test connection by listing databases
            list(self.client.list_databases())
            self.connected = True
            return True, "Connected successfully"
        
        except exceptions.CosmosHttpResponseError as e:
            self.connected = False
            return False, f"Connection failed: {str(e)}"
        except Exception as e:
            self.connected = False
            return False, f"Unexpected error: {str(e)}"
    
    def disconnect(self):
        """Disconnect from Cosmos DB"""
        self.client = None
        self.config = None
        self.connected = False
    
    def get_databases(self) -> List[str]:
        """
        Get list of database names
        
        Returns:
            List of database names
        """
        if not self.connected or not self.client:
            return []
        
        try:
            databases = list(self.client.list_databases())
            return [db['id'] for db in databases]
        except Exception as e:
            print(f"Error fetching databases: {e}")
            return []
    
    def get_containers(self, database_name: str) -> List[str]:
        """
        Get list of container names in a database
        
        Args:
            database_name: Name of the database
            
        Returns:
            List of container names
        """
        if not self.connected or not self.client:
            return []
        
        try:
            database = self.client.get_database_client(database_name)
            containers = list(database.list_containers())
            return [container['id'] for container in containers]
        except Exception as e:
            print(f"Error fetching containers: {e}")
            return []
    
    def query_items(
        self, 
        database_name: str, 
        container_name: str, 
        query: str = "SELECT * FROM c",
        max_items: int = 1000
    ) -> List[Dict[str, Any]]:
        """
        Query items from a container
        
        Args:
            database_name: Name of the database
            container_name: Name of the container
            query: SQL query string
            max_items: Maximum number of items to retrieve
            
        Returns:
            List of items
        """
        if not self.connected or not self.client:
            return []
        
        try:
            database = self.client.get_database_client(database_name)
            container = database.get_container_client(container_name)
            
            items = list(container.query_items(
                query=query,
                enable_cross_partition_query=True,
                max_item_count=max_items
            ))
            
            return items
        except Exception as e:
            print(f"Error querying items: {e}")
            return []
    
    def get_all_items(
        self, 
        database_name: str, 
        container_name: str,
        max_items: int = 1000
    ) -> List[Dict[str, Any]]:
        """
        Get all items from a container
        
        Args:
            database_name: Name of the database
            container_name: Name of the container
            max_items: Maximum number of items to retrieve
            
        Returns:
            List of items
        """
        return self.query_items(database_name, container_name, "SELECT * FROM c", max_items)
