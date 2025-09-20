"""
Yardee Python SDK - Official Python client for Yardee Vector Database API.
"""

import json
import time
from typing import Dict, List, Optional, Union, Any
from urllib.parse import urljoin

try:
    import requests
except ImportError:
    raise ImportError(
        "The 'requests' library is required. Install it with: pip install requests"
    )


class YardeeError(Exception):
    """Base exception for Yardee SDK errors."""
    pass


class AuthenticationError(YardeeError):
    """Raised when API authentication fails."""
    pass


class APIError(YardeeError):
    """Raised when API returns an error response."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, response_data: Optional[Dict] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class RateLimitError(YardeeError):
    """Raised when API rate limit is exceeded."""
    pass


class Client:
    """
    Yardee API Client for vector database operations.
    
    This client provides access to Yardee's vector database API, including
    knowledge base management, document upload, and semantic search.
    
    Args:
        api_key: Your Yardee API key (get one at https://app.yardee.ai)
        base_url: API base URL (default: https://app.yardee.ai/api/v1)
        timeout: Request timeout in seconds (default: 30)
        max_retries: Maximum number of retries for failed requests (default: 3)
    
    Example:
        >>> client = Client(api_key="sk-your-api-key")
        >>> results = client.search(knowledge_base_id=123, query="customer support")
        >>> print(f"Found {len(results['results'])} results")
    """
    
    def __init__(
        self,
        api_key: str,
        base_url: str = "https://app.yardee.ai/api/v1",
        timeout: int = 30,
        max_retries: int = 3,
    ):
        if not api_key:
            raise ValueError("API key is required")
        
        if not api_key.startswith("sk-"):
            raise ValueError("API key must start with 'sk-'")
        
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        
        # Set up session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "yardee-python-sdk/0.1.1"
        })
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the API with automatic retries and error handling.
        """
        url = urljoin(f"{self.base_url}/", endpoint.lstrip("/"))
        
        # Prepare request kwargs
        kwargs = {
            "timeout": self.timeout,
            "params": params,
        }
        
        if files:
            # For file uploads, don't set Content-Type (requests will set it)
            headers = self.session.headers.copy()
            del headers["Content-Type"]
            kwargs["headers"] = headers
            kwargs["files"] = files
            if data:
                kwargs["data"] = data
        elif data:
            kwargs["json"] = data
        
        # Retry logic
        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                response = self.session.request(method, url, **kwargs)
                
                # Handle rate limiting with exponential backoff
                if response.status_code == 429:
                    if attempt < self.max_retries:
                        wait_time = 2 ** attempt
                        time.sleep(wait_time)
                        continue
                    else:
                        raise RateLimitError("Rate limit exceeded. Please try again later.")
                
                # Handle other HTTP errors
                if response.status_code == 401:
                    raise AuthenticationError("Invalid API key")
                
                if response.status_code >= 400:
                    try:
                        error_data = response.json()
                        error_message = error_data.get("error", f"HTTP {response.status_code}")
                    except (ValueError, KeyError):
                        error_message = f"HTTP {response.status_code}: {response.text}"
                    
                    raise APIError(
                        error_message,
                        status_code=response.status_code,
                        response_data=error_data if 'error_data' in locals() else None
                    )
                
                # Parse successful response
                try:
                    return response.json()
                except ValueError:
                    return {"success": True, "data": response.text}
                
            except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
                last_exception = e
                if attempt < self.max_retries:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                    continue
                else:
                    raise YardeeError(f"Request failed after {self.max_retries} retries: {str(e)}")
        
        # This should never be reached, but just in case
        raise YardeeError(f"Request failed: {str(last_exception)}")
    
    def search(
        self,
        knowledge_base_id: int,
        query: str,
        top_k: int = 5,
        similarity_threshold: float = 0.1,
        use_mmr: bool = True,
        metadata_filters: Optional[Dict] = None,
        chat_history: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """
        Perform semantic search across a knowledge base.
        
        Args:
            knowledge_base_id: ID of the knowledge base to search
            query: Search query text
            top_k: Maximum number of results to return (default: 5)
            similarity_threshold: Minimum similarity score (default: 0.1)
            use_mmr: Use Maximum Marginal Relevance for diversity (default: True)
            metadata_filters: Optional filters by document metadata
            chat_history: Optional chat history for structured data queries
        
        Returns:
            Dictionary containing search results with 'results' and 'total_results' keys
        
        Example:
            >>> results = client.search(
            ...     knowledge_base_id=123,
            ...     query="How do I reset my password?",
            ...     top_k=3
            ... )
            >>> for result in results['results']:
            ...     print(f"Score: {result.get('similarity_score', 'N/A')}")
            ...     print(f"Content: {result['content'][:100]}...")
        """
        data = {
            "query": query,
            "top_k": top_k,
            "similarity_threshold": similarity_threshold,
            "use_mmr": use_mmr,
        }
        
        if metadata_filters:
            data["metadata_filters"] = metadata_filters
        
        if chat_history:
            data["chat_history"] = chat_history
        
        return self._make_request(
            "POST",
            f"knowledgebases/{knowledge_base_id}/search/",
            data=data
        )
    
    def list_knowledge_bases(self) -> Dict[str, Any]:
        """
        List all knowledge bases in your account.
        
        Returns:
            Dictionary containing 'knowledge_bases' list and 'count'
        
        Example:
            >>> kbs = client.list_knowledge_bases()
            >>> print(f"You have {kbs['count']} knowledge bases")
            >>> for kb in kbs['knowledge_bases']:
            ...     print(f"- {kb['name']} (ID: {kb['id']})")
        """
        return self._make_request("GET", "knowledgebases/")
    
    def create_knowledge_base(self, name: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new knowledge base.
        
        Args:
            name: Name of the knowledge base
            description: Optional description
        
        Returns:
            Dictionary containing the created knowledge base details
        
        Example:
            >>> kb = client.create_knowledge_base(
            ...     name="Customer Support",
            ...     description="FAQ and support documents"
            ... )
            >>> print(f"Created knowledge base with ID: {kb['id']}")
        """
        data = {"name": name}
        if description:
            data["description"] = description
        
        return self._make_request("POST", "knowledgebases/", data=data)
    
    def get_knowledge_base(self, knowledge_base_id: int) -> Dict[str, Any]:
        """
        Get details of a specific knowledge base.
        
        Args:
            knowledge_base_id: ID of the knowledge base
        
        Returns:
            Dictionary containing knowledge base details
        """
        return self._make_request("GET", f"knowledgebases/{knowledge_base_id}/")
    
    def update_knowledge_base(
        self, 
        knowledge_base_id: int, 
        name: Optional[str] = None, 
        description: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Update a knowledge base.
        
        Args:
            knowledge_base_id: ID of the knowledge base
            name: Optional new name
            description: Optional new description
        
        Returns:
            Dictionary containing updated knowledge base details
        
        Example:
            >>> updated_kb = client.update_knowledge_base(
            ...     knowledge_base_id=123,
            ...     name="Updated Name",
            ...     description="New description"
            ... )
        """
        data = {}
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        
        if not data:
            raise ValueError("At least one of 'name' or 'description' must be provided")
        
        return self._make_request("PUT", f"knowledgebases/{knowledge_base_id}/", data=data)
    
    def upload_document(
        self,
        knowledge_base_id: int,
        file_path: str,
        filename: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Upload a document to a knowledge base.
        
        Args:
            knowledge_base_id: ID of the target knowledge base
            file_path: Path to the file to upload
            filename: Optional custom filename (defaults to file_path basename)
        
        Returns:
            Dictionary containing upload details and document ID
        
        Example:
            >>> result = client.upload_document(
            ...     knowledge_base_id=123,
            ...     file_path="./documents/faq.pdf"
            ... )
            >>> print(f"Uploaded document ID: {result['id']}")
        """
        import os
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if filename is None:
            filename = os.path.basename(file_path)
        
        with open(file_path, "rb") as f:
            files = {"file": (filename, f)}
            return self._make_request(
                "POST",
                f"knowledgebases/{knowledge_base_id}/documents/upload/",
                files=files
            )
    
    def list_documents(self, knowledge_base_id: int) -> Dict[str, Any]:
        """
        List all documents in a knowledge base.
        
        Args:
            knowledge_base_id: ID of the knowledge base
        
        Returns:
            Dictionary containing 'documents' list and 'count'
        """
        return self._make_request("GET", f"knowledgebases/{knowledge_base_id}/documents/")
    
    def delete_document(self, document_id: int) -> Dict[str, Any]:
        """
        Delete a document from a knowledge base.
        
        Args:
            document_id: ID of the document to delete
        
        Returns:
            Dictionary confirming deletion
        """
        return self._make_request("DELETE", f"documents/{document_id}/")
    
    # Connection Management Methods
    
    def create_database_connection(
        self,
        knowledge_base_id: int,
        name: str,
        db_type: str,
        host: str,
        port: int,
        database: str,
        username: str,
        password: str,
        ssl_required: bool = True,
        use_ssh_tunnel: bool = False,
        ssh_host: Optional[str] = None,
        ssh_port: Optional[int] = None,
        ssh_user: Optional[str] = None,
        ssh_password: Optional[str] = None,
        ssh_private_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a live database connection for real-time querying.
        
        Args:
            knowledge_base_id: ID of the target knowledge base
            name: Connection nickname (e.g., "Production DB")
            db_type: Database type ("postgres", "mysql", "sqlserver")
            host: Database host (e.g., "db.example.com")
            port: Database port (e.g., 5432 for PostgreSQL)
            database: Database name
            username: Database username (preferably read-only)
            password: Database password
            ssl_required: Whether to enforce SSL connection (default: True)
            use_ssh_tunnel: Whether to use SSH tunnel (default: False)
            ssh_host: SSH host (required if use_ssh_tunnel=True)
            ssh_port: SSH port (required if use_ssh_tunnel=True)  
            ssh_user: SSH username (required if use_ssh_tunnel=True)
            ssh_password: SSH password (optional, use with ssh_private_key)
            ssh_private_key: SSH private key content (optional, use with ssh_password)
        
        Returns:
            Dictionary containing connection details and ID
        
        Example:
            >>> conn = client.create_database_connection(
            ...     knowledge_base_id=123,
            ...     name="Production PostgreSQL",
            ...     db_type="postgres",
            ...     host="db.mycompany.com",
            ...     port=5432,
            ...     database="analytics",
            ...     username="readonly_user",
            ...     password="secure_password"
            ... )
            >>> print(f"Database connection created with ID: {conn['id']}")
        """
        data = {
            "name": name,
            "db_type": db_type,
            "host": host,
            "port": port,
            "database": database,
            "username": username,
            "password": password,
            "ssl_required": ssl_required,
        }
        
        if use_ssh_tunnel:
            if not all([ssh_host, ssh_port, ssh_user]):
                raise ValueError("ssh_host, ssh_port, and ssh_user are required when use_ssh_tunnel=True")
            
            data.update({
                "use_ssh_tunnel": True,
                "ssh_host": ssh_host,
                "ssh_port": ssh_port,
                "ssh_user": ssh_user,
            })
            
            if ssh_password:
                data["ssh_password"] = ssh_password
            if ssh_private_key:
                data["ssh_private_key"] = ssh_private_key
        
        return self._make_request("POST", f"knowledgebases/{knowledge_base_id}/database-connections/", data=data)
    
    def create_hubspot_connection(
        self,
        knowledge_base_id: int,
        name: str,
        private_app_token: str,
    ) -> Dict[str, Any]:
        """
        Create a HubSpot CRM connection for real-time data querying.
        
        Args:
            knowledge_base_id: ID of the target knowledge base
            name: Connection nickname (e.g., "HubSpot CRM")
            private_app_token: HubSpot Private App Token for authentication
        
        Returns:
            Dictionary containing connection details and ID
        
        Example:
            >>> conn = client.create_hubspot_connection(
            ...     knowledge_base_id=123,
            ...     name="HubSpot CRM",
            ...     private_app_token="pat-na1-your-token-here"
            ... )
            >>> print(f"HubSpot connection created with ID: {conn['id']}")
        
        Note:
            To get a HubSpot Private App Token:
            1. Go to HubSpot Settings → Integrations → Private Apps
            2. Create a new private app
            3. Set required scopes: crm.objects.contacts.read, crm.objects.deals.read, 
               crm.objects.companies.read, tickets (if needed)
            4. Copy the generated token
        """
        data = {
            "name": name,
            "db_type": "hubspot",
            "auth_type": "private_app_token",
            "hubspot_private_app_token": private_app_token,
        }
        
        return self._make_request("POST", f"knowledgebases/{knowledge_base_id}/database-connections/", data=data)
    
    def list_connections(self, knowledge_base_id: int) -> Dict[str, Any]:
        """
        List all connections (database and HubSpot) for a knowledge base.
        
        Args:
            knowledge_base_id: ID of the knowledge base
        
        Returns:
            Dictionary containing list of connections
        
        Example:
            >>> connections = client.list_connections(123)
            >>> for conn in connections['connections']:
            ...     print(f"- {conn['name']} ({conn['db_type']}) - {conn['status']}")
        """
        return self._make_request("GET", f"knowledgebases/{knowledge_base_id}/database-connections/")
    
    def get_connection(self, knowledge_base_id: int, connection_id: int) -> Dict[str, Any]:
        """
        Get details of a specific connection.
        
        Args:
            knowledge_base_id: ID of the knowledge base
            connection_id: ID of the connection
        
        Returns:
            Dictionary containing connection details
        """
        return self._make_request("GET", f"knowledgebases/{knowledge_base_id}/database-connections/{connection_id}/")
    
    def update_connection(
        self,
        knowledge_base_id: int,
        connection_id: int,
        name: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Update a connection's settings.
        
        Args:
            knowledge_base_id: ID of the knowledge base
            connection_id: ID of the connection
            name: Optional new connection name
            **kwargs: Other connection fields to update
        
        Returns:
            Dictionary containing updated connection details
        """
        data = {}
        if name is not None:
            data["name"] = name
        data.update(kwargs)
        
        if not data:
            raise ValueError("At least one field must be provided for update")
        
        return self._make_request("PUT", f"knowledgebases/{knowledge_base_id}/database-connections/{connection_id}/", data=data)
    
    def delete_connection(self, knowledge_base_id: int, connection_id: int) -> Dict[str, Any]:
        """
        Delete a connection.
        
        Args:
            knowledge_base_id: ID of the knowledge base
            connection_id: ID of the connection to delete
        
        Returns:
            Dictionary confirming deletion
        """
        return self._make_request("DELETE", f"knowledgebases/{knowledge_base_id}/database-connections/{connection_id}/")
    
    def test_connection(self, knowledge_base_id: int, connection_id: int) -> Dict[str, Any]:
        """
        Test a database or HubSpot connection.
        
        Args:
            knowledge_base_id: ID of the knowledge base
            connection_id: ID of the connection to test
        
        Returns:
            Dictionary with test results
        
        Example:
            >>> result = client.test_connection(123, 456)
            >>> if result['success']:
            ...     print("✅ Connection is working!")
            ... else:
            ...     print(f"❌ Connection failed: {result['error']}")
        """
        return self._make_request("POST", f"knowledgebases/{knowledge_base_id}/database-connections/{connection_id}/test/")
    
    def close(self):
        """Close the HTTP session."""
        if hasattr(self, 'session'):
            self.session.close()
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
