"""
DocWal Python SDK

Official Python SDK for DocWal API - Issue and manage verifiable digital credentials.
"""

from .client import DocWalClient
from .exceptions import DocWalError, AuthenticationError, ValidationError, RateLimitError

__version__ = "1.0.1"
__all__ = [
    "DocWalClient",
    "DocWalError",
    "AuthenticationError",
    "ValidationError",
    "RateLimitError",
]
