"""
Connection configuration model for Azure Cosmos DB
"""


class ConnectionConfig:
    """Model for storing Azure Cosmos DB connection configuration"""
    
    def __init__(
        self,
        cosmos_endpoint: str = "",
        service_url: str = "",
        client_id: str = "",
        client_secret: str = "",
        resource: str = "https://cosmos.azure.com",
        grant_type: str = "client_credentials"
    ):
        self.cosmos_endpoint = cosmos_endpoint
        self.service_url = service_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.resource = resource
        self.grant_type = grant_type
    
    def is_valid(self) -> bool:
        """Check if the connection configuration is valid"""
        return bool(
            self.cosmos_endpoint and
            self.service_url and
            self.client_id and
            self.client_secret and
            self.resource
        )
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary"""
        return {
            'cosmos_endpoint': self.cosmos_endpoint,
            'service_url': self.service_url,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'resource': self.resource,
            'grant_type': self.grant_type
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ConnectionConfig':
        """Create configuration from dictionary"""
        return cls(
            cosmos_endpoint=data.get('cosmos_endpoint', ''),
            service_url=data.get('service_url', ''),
            client_id=data.get('client_id', ''),
            client_secret=data.get('client_secret', ''),
            resource=data.get('resource', 'https://cosmos.azure.com'),
            grant_type=data.get('grant_type', 'client_credentials')
        )
