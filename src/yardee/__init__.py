"""
Yardee Python SDK

Official Python client library for the Yardee Vector Database API.

Get started:
    pip install yardee

Usage:
    from yardee import Client
    
    client = Client(api_key="sk-your-api-key")
    results = client.search(knowledge_base_id=123, query="your question")

Get your API key at: https://app.yardee.ai
"""

from .client import Client, YardeeError, AuthenticationError, APIError, RateLimitError

__version__ = "0.1.0"
__author__ = "Yardee Team"
__email__ = "support@yardee.ai"
__all__ = [
    "Client",
    "YardeeError", 
    "AuthenticationError",
    "APIError",
    "RateLimitError",
]

# For convenience - commonly used functions
def search(api_key: str, knowledge_base_id: int, query: str, **kwargs):
    """
    Quick search function for one-off queries.
    
    Args:
        api_key: Your Yardee API key
        knowledge_base_id: ID of the knowledge base to search
        query: Search query text
        **kwargs: Additional search parameters
    
    Returns:
        Search results dictionary
    
    Example:
        >>> from yardee import search
        >>> results = search("sk-your-key", 123, "How do I login?")
    """
    with Client(api_key) as client:
        return client.search(knowledge_base_id, query, **kwargs)
